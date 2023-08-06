import time
from threading import Thread, Lock

import bidict
import numpy as np
import smaract.picoscale as ps
import smaract.si as si

from kamzik3 import DeviceError
from kamzik3.constants import *
from kamzik3.devices.device import Device
from kamzik3.devices.deviceChannel import DeviceChannel
from kamzik3.snippets.snippetsDecorators import expose_method
from kamzik3.snippets.snippetsTimer import PreciseCallbackTimer

use_data_source_types = {
    si.DataSource.POSITION: "Position",
    si.DataSource.TEMPERATURE: "Temperature",
    si.DataSource.HUMIDITY: "Humidity",
    si.DataSource.PRESSURE: "Pressure"
}

datatypes = {
    si.DataType.INT8: np.int8,
    si.DataType.UINT8: np.uint8,
    si.DataType.INT16: np.int16,
    si.DataType.UINT16: np.uint16,
    si.DataType.INT32: np.int32,
    si.DataType.UINT32: np.uint32,
    si.DataType.INT48: np.int64,
    si.DataType.UINT48: np.uint64,
    si.DataType.INT64: np.int64,
    si.DataType.UINT64: np.uint64,
    si.DataType.FLOAT32: np.float32,
    si.DataType.FLOAT64: np.float64,
    si.DataType.FLOAT64: str,
}

si_units = {
    si.BaseUnit.METRE: "m",
    si.BaseUnit.NO: None,
    si.BaseUnit.DEGREE: "deg",
    si.BaseUnit.DEGREE_CELSIUS: "degC",
    si.BaseUnit.AMPERE: "A",
    si.BaseUnit.HERTZ: "Hz",
    si.BaseUnit.KELVIN: "k",
    si.BaseUnit.KILOGRAM: "Kg",
    si.BaseUnit.PERCENT: "%",
    si.BaseUnit.SECOND: "s",
    si.BaseUnit.WATT: "W",
    si.BaseUnit.VOLT: "V",
    si.BaseUnit.PASCAL: "Pa",
}

streaming_modes = bidict.FrozenOrderedBidict({
    si.StreamingMode.DIRECT: "Direct",
    si.StreamingMode.TRIGGERED: "Triggered",
})

GROUP_STREAMING = "Streaming"


class DevicePicoscale(Device):
    # Increase connection timeout, since this Device takes it's time.
    # Usually it takes about 20 seconds.
    # To be safe, set connection timeout to 25 seconds
    connection_timeout = 25000
    polling = False
    polling_timer = None

    def __init__(self, locator, device_id=None, config=None):
        """
        Locator defines where to find Picoscale unit.
        From documentation some examples:
            usb:ix:0
            network:192.168.1.100:55555
        @param locator: locator address
        @type locator: str
        @param device_id: device ID
        @type device_id: str
        @param config: config dict
        @type config: dict
        """
        self.locator = locator
        self.handle = None
        self.polled_functions = []
        self.stream_sources = []
        self.stream_buffers = {}
        self.readout_lock = Lock()
        Device.__init__(self, device_id, config)
        self.connect()

    def connect(self, *args):
        """
        Use si.open to connect to PicoScale.
        It returns handle.
        According to what we observer, only one client can be connected at the same time.
        It's also taking a long time to connect. At some cases close to 20 seconds.
        :param args: connect attributes
        """
        try:
            self.connecting = True
            self.connected = False
            self.device_connection_poller.add_connecting_device(self)
            self.handle = si.Open(self.locator)
            self.handle_connect_event()
        except si.Error as e:
            self.logger.exception(f"Connection exception: {self._get_exception(e)}")
        except DeviceError:
            self.logger.exception(u"Connection exception")
            return

    def _init_attributes(self):
        Device._init_attributes(self)
        self.create_attribute(ATTR_SERIAL_NUMBER, readonly=True)
        self.create_attribute(ATTR_CHANNELS, readonly=True, default_type=np.uint16)
        self.create_attribute(ATTR_FULL_ACCESS, default_value=True, default_type=bool,
                              set_function=self.set_full_access)
        self.create_attribute(ATTR_PILOT_LASER, default_value=False, default_type=bool,
                              set_function=self.set_pilot_laser)
        self.create_attribute(ATTR_IS_STABLE, readonly=True, default_type=bool)
        self.create_attribute(ATTR_FRAME_AGGREGATION, group=GROUP_STREAMING, default_value=1, default_type=np.uint32,
                              set_function=self.set_frame_aggregation, min_value=1, max_value=1)
        self.create_attribute(ATTR_FRAMERATE, group=GROUP_STREAMING, default_value=1, default_type=np.uint32,
                              set_function=self.set_frame_rate, unit="Hz", min_value=1, max_value=10e6)
        self.create_attribute(ATTR_BUFFER_AGGREGATION, group=GROUP_STREAMING, default_value=0, default_type=np.uint32,
                              set_function=self.set_buffer_aggregation, min_value=0)
        self.create_attribute(ATTR_STREAMING_MODE, group=GROUP_STREAMING,
                              default_value=streaming_modes[si.StreamingMode.DIRECT],
                              default_type=list(streaming_modes.values()), set_function=self.set_streaming_mode)
        self.create_attribute(ATTR_BUFFERS_INTERLEAVED, group=GROUP_STREAMING, default_value=False, default_type=bool,
                              set_function=self.set_buffers_interleaved)
        self.create_attribute(ATTR_FILTER_RATE, group=GROUP_STREAMING, default_value=10e6, default_type=np.float64,
                              set_function=self.set_filter_rate, min_value=1, max_value=10e6, unit="Hz")
        self.create_attribute(ATTR_BUFFERS_COUNT, group=GROUP_STREAMING, default_value=2, default_type=np.uint32,
                              set_function=self.set_buffers_count, min_value=2, max_value=255)

    def handle_configuration(self):
        start_at = time.time()
        self._config_commands()
        self._config_attributes()
        self.set_full_access(True)
        serial_number = si.GetProperty_s(self.handle, si.EPK(si.Property.DEVICE_SERIAL_NUMBER, 0, 0))
        self.set_value(ATTR_SERIAL_NUMBER, serial_number)
        number_of_channels = si.GetProperty_i32(self.handle, si.EPK(si.Property.NUMBER_OF_CHANNELS, 0, 0))
        self.set_value(ATTR_CHANNELS, number_of_channels)
        self.get_pilot_laser()
        self.get_system_stable()
        self.start_polling()
        self.set_status(STATUS_CONFIGURED)
        self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

    def set_buffers_count(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.NUMBER_OF_STREAMBUFFERS, 0, 0), int(value))
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_buffers_interleaved(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMBUFFERS_INTERLEAVED, 0, 0), int(value))
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_filter_rate(self, value):
        try:
            si.SetProperty_f64(self.handle, si.EPK(ps.Property.SYS_FILTER_RATE, 0, 0), value)
            real_filter_rate = si.GetProperty_f64(self.handle, si.EPK(ps.Property.SYS_FILTER_RATE, 0, 0))
            self.set_raw_value([GROUP_STREAMING, ATTR_FILTER_RATE], real_filter_rate)
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_frame_aggregation(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.FRAME_AGGREGATION, 0, 0), int(value))
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_buffer_aggregation(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMBUFFER_AGGREGATION, 0, 0), int(value))
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_frame_rate(self, value : int) -> None:
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.FRAME_RATE, 0, 0), int(value))
            real_frame_rate = si.GetProperty_f64(self.handle, si.EPK(si.Property.PRECISE_FRAME_RATE, 0, 0))
            self.set_raw_value([GROUP_STREAMING, ATTR_FRAMERATE], real_frame_rate)
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    def set_streaming_mode(self, value : str) -> None:
        value = streaming_modes.inv[value]
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_MODE, 0, 0), value)
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    @expose_method({"clear_values": "Clear previous streamed values"})
    def start_streaming(self, clear_values : bool = True) -> None:
        try:
            clear_values = bool(int(clear_values))
            self.stream_sources = sorted(self.stream_sources, key=lambda element: (element[0], element[1]))
            for channel, source in self.stream_sources:
                if clear_values:
                    self.notify((channel, source, ATTR_STREAM_READOUT), None)
                self.stream_buffers[(channel, source)] = []
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.SG_CLOCK_SOURCE, 0, 0),
                               ps.StreamGeneratorSource.INTERNAL)
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_MODE, 0, 0), si.StreamingMode.DIRECT)
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_ACTIVE, 0, 0), si.ENABLED)
            self.set_status(STATUS_BUSY)
            Thread(target=self.stream_data_thread).start()
        except si.Error as e:
            raise DeviceError(self._get_exception(e))


    @expose_method()
    def setup_triggered_stream(self) -> None:
        """
        Prepare triggered stream, that expects HW TTL signal _|¯¯¯¯|_.
        Setup inputs and outputs to collect streamed data for width of TTL pulse.
        :return: None
        """
        try:
            # Setup source of Trigger 0 and 1 to External Trigger
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_SOURCE_EVENT, 0, 0),
                               ps.TriggerEvent.EXTERNAL_TRIGGER)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_SOURCE_EVENT, 1, 0),
                               ps.TriggerEvent.EXTERNAL_TRIGGER)

            # Setup Trigger output to Immediate and don't reset stream at next trigger for trigger output 0 and 1
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_OUTPUT_MODE, 0, 0),
                               ps.TriggerOutputMode.IMMEDIATE_NO_RESET)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_OUTPUT_MODE, 1, 0),
                               ps.TriggerOutputMode.IMMEDIATE_NO_RESET)

            # Setup Trigger start index to 0
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.SG_TRIGGER_START_INDEX, 0, 0), 0)
            # Setup Trigger stop index to 0
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.SG_TRIGGER_STOP_INDEX, 0, 0), 1)

            # Expect Positive Level on Trigger input 0 - start of Trigger pulse, high level of TTL signal _|¯¯
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_SOURCE_CONDITION, 0, 0),
                               ps.TriggerCondition.POSITIVE_LEVEL)
            # Expect Negative Level on Trigger input 0 - end of Trigger pulse, low level of TTL signal ¯¯|_
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_SOURCE_CONDITION, 1, 0),
                               ps.TriggerCondition.NEGATIVE_LEVEL)
            # Set Trigger logic for both trigger inputs to OR
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_LOGIC_OPERATION, 0, 0),
                               ps.TriggerLogicOperation.OR)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_LOGIC_OPERATION, 1, 0),
                               ps.TriggerLogicOperation.OR)
            # Set Trigger OR and AND mask for both trigger inputs
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_AND_MASK, 0, 0), 1)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_OR_MASK, 0, 0), 1)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_AND_MASK, 1, 0), 2)
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_OR_MASK, 1, 0), 2)

            # Set streaming mode to Trigger
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_MODE, 0, 0), si.StreamingMode.TRIGGERED)
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    @expose_method({"clear_values": "Clear previous streamed values"})
    def wait_for_trigger(self, clear_values: bool = True) -> None :
        """

        """
        try:
            clear_values = bool(int(clear_values))
            for channel, source in self.stream_sources:
                if clear_values:
                    self.notify((channel, source, ATTR_STREAM_READOUT), None)
                self.stream_buffers[(channel, source)] = []

            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_ACTIVE, 0, 0), si.ENABLED)
            self.set_status(STATUS_BUSY)
            Thread(target=self.stream_data_thread).start()
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    @expose_method()
    def stop_streaming(self):
        try:
            si.SetProperty_i32(self.handle, si.EPK(si.Property.STREAMING_ACTIVE, 0, 0), si.DISABLED)
            # self.set_value([GROUP_STREAMING, ATTR_STREAMING_MODE], streaming_modes[si.StreamingMode.DIRECT])
            # si.SetProperty_i32(self.handle, si.EPK(ps.Property.SG_CLOCK_SOURCE, 0, 0),
            #                    ps.StreamGeneratorSource.INTERNAL)
            self.set_status(STATUS_IDLE)
        except si.Error as e:
            raise DeviceError(self._get_exception(e))

    @expose_method()
    def reset_streaming(self):
        si.ResetStreamingConfiguration(self.handle)
        self.set_value([ATTR_STREAMING, ATTR_FRAMERATE], 1)
        self.set_value([ATTR_STREAMING, ATTR_FILTER_RATE], 1)
        self.set_value([ATTR_STREAMING, ATTR_BUFFERS_COUNT], 2)
        self.set_value([ATTR_STREAMING, ATTR_FRAME_AGGREGATION], 1)

    def set_full_access(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.SYS_FULL_ACCESS_CONNECTION, 0, 0), int(value))
        except si.Error as e:
            self.get_full_access()
            raise DeviceError(self._get_exception(e))

    def set_pilot_laser(self, value):
        try:
            si.SetProperty_i32(self.handle, si.EPK(ps.Property.SYS_PILOT_LASER_ACTIVE, 0, 0), int(value))
        except si.Error as e:
            self.get_pilot_laser()
            raise DeviceError(self._get_exception(e))

    @staticmethod
    def _get_exception(exception):
        """
        Helper method to obtain Exception info from PicoScale.
        :param exception: thrown exception
        :type exception: Exception
        :return: Exception message
        :rtype: str
        """
        err_name = "(0x{:04X})".format(exception.code)
        if exception.code in set(err.value for err in si.ErrorCode):
            err_name = si.ErrorCode(exception.code).name + " " + err_name
        elif exception.code in set(err.value for err in ps.ErrorCode):
            err_name = ps.ErrorCode(exception.code).name + " " + err_name
        return f"SI {exception.func} error: {err_name}."

    def process_buffer(self, buffer):
        """
        Processes the contents of a buffer received from the API.
        This function would typically e.g. store the data to disc.
        In this example the data is stored in a buffer for later
        processing.
        """
        for source_index in range(buffer.info.numberOfSources):
            values = si.CopyBuffer(self.handle, buffer.info.bufferId, source_index)
            channel, source = self.stream_sources[source_index]
            self.stream_buffers[(channel, source)] += values
        si.ReleaseBuffer(self.handle, buffer.info.bufferId)
        return values == []

    def stream_data_thread(self):
        with self.readout_lock:
            timeout = si.TIMEOUT_INFINITE
            last_buffer_empty = False
            stream_stopped = False
            while True:
                try:
                    ev = si.WaitForEvent(self.handle, timeout)
                    if ev.type == si.EventType.STREAMBUFFER_READY:
                        # get buffer data
                        buffer = si.AcquireBuffer(self.handle, ev.bufferId)
                        last_buffer_empty = self.process_buffer(buffer)
                        if last_buffer_empty and stream_stopped:
                            break
                    elif ev.type in (si.EventType.STREAM_STOPPED, si.EventType.STREAM_ABORTED):
                        stream_stopped = True
                        if last_buffer_empty:
                            break
                        timeout = 100
                        continue
                    else:
                        print("Received unexpected event type: {} (parameter: {})".format(ev.type, ev.devEventParameter))
                        break
                except si.bindings.Error:
                    break

            for channel, source in self.stream_sources:
                self.notify((channel, source, ATTR_STREAM_READOUT), self.stream_buffers[(channel, source)])

    def close(self):
        """
        To properly close PicoScale, we need to close handle.
        Otherwise we cannot connect to Device again.
        """
        try:
            if self.handle is not None:
                si.Close(self.handle)
        except Exception as e:
            pass
        finally:
            self.handle = None
        Device.close(self)

    def get_full_access(self):
        pilot_laser = si.GetProperty_i32(self.handle, si.EPK(ps.Property.SYS_FULL_ACCESS_CONNECTION, 0, 0))
        self.set_value(ATTR_FULL_ACCESS, pilot_laser)

    def get_pilot_laser(self):
        pilot_laser = si.GetProperty_i32(self.handle, si.EPK(ps.Property.SYS_PILOT_LASER_ACTIVE, 0, 0))
        self.set_value(ATTR_PILOT_LASER, pilot_laser)

    def get_system_stable(self):
        is_stable = si.GetProperty_i32(self.handle, si.EPK(ps.Property.SYS_IS_STABLE, 0, 0))
        self.set_value(ATTR_IS_STABLE, is_stable)

    def get_trigger_state(self):
        trigger_state = si.GetProperty_i32(self.handle, si.EPK(ps.Property.TRIGGER_STATE, 0, 0))
        print(trigger_state)

    def poller_interval(self):
        for fun in self.polled_functions:
            fun()

    def start_polling(self):
        self.polling = True
        self.polled_functions = [self.get_system_stable]
        self.polling_timer = PreciseCallbackTimer(300, self.poller_interval)
        self.polling_timer.start()

    def stop_polling(self):
        self.polling = False
        self.polling_timer.stop()


class DevicePicoscaleChannel(DeviceChannel):
    polling = False
    polling_timer = None

    def __init__(self, device, channel, device_id=None, config=None):
        self.polled_functions = []
        self.source_groups = {}
        DeviceChannel.__init__(self, device, channel, device_id, config)

    def _init_attributes(self):
        DeviceChannel._init_attributes(self)
        self.create_attribute(ATTR_SOURCES_COUNT, readonly=True)

    def handle_configuration(self):
        if self.configured:
            return

        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.configured = True
            self.start_polling()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        self.connected = True
        number_of_data_sources = si.GetProperty_i32(self.device.handle,
                                                    si.EPK(si.Property.NUMBER_OF_DATA_SOURCES, self.channel, 0))
        self.set_value(ATTR_SOURCES_COUNT, number_of_data_sources)
        self._configure_sources()
        _finish_configuration()

    def _configure_sources(self):
        self.source_groups.clear()
        prefix = {-12: u"p", -9: u"n", -6: u"u", -3: u"m"}

        for source_index in range(self.get_value(ATTR_SOURCES_COUNT)):
            ds_type = si.GetProperty_i32(self.device.handle,
                                         si.EPK(si.Property.DATA_SOURCE_TYPE, self.channel, source_index))
            if ds_type in use_data_source_types:
                data_type = si.GetProperty_i32(self.device.handle,
                                               si.EPK(si.Property.DATA_TYPE, self.channel, source_index))
                base_unit = si.GetProperty_i32(self.device.handle,
                                               si.EPK(si.Property.BASE_UNIT, self.channel, source_index))
                base_resolution = si.GetProperty_i32(self.device.handle,
                                                     si.EPK(si.Property.BASE_RESOLUTION, self.channel,
                                                            source_index))
                streamable = si.GetProperty_i32(self.device.handle,
                                                si.EPK(si.Property.IS_STREAMABLE, self.channel, source_index))
                group_name = f"{use_data_source_types[ds_type]}"
                self.source_groups[source_index] = group_name
                si_unit = si_units.get(base_unit, None)
                base_unit = prefix.get(base_resolution, "") + si_unit
                self.create_attribute(ATTR_VALUE_READOUT, default_type=np.float64,
                                      unit=base_unit, group=group_name,
                                      readonly=True, decimals=10)
                self.create_attribute(ATTR_ID, group=group_name, default_value=source_index, readonly=True,
                                      default_type=np.uint16)
                streaming_enabled = si.GetProperty_i32(self.device.handle,
                                                       si.EPK(si.Property.STREAMING_ENABLED, self.channel,
                                                              source_index))
                self.create_attribute(ATTR_ALLOW_STREAM, default_value=streaming_enabled, group=group_name,
                                      default_type=bool,
                                      set_function=lambda v, source_index=source_index: self.set_allow_streaming(
                                          source_index, v))
                if bool(streamable):
                    self.create_attribute(ATTR_STREAM_READOUT, default_value=[], default_type=TYPE_ARRAY,
                                          group=group_name, readonly=True, streaming_enabled=False,
                                          unit=base_unit, display=False)

    def subject_update(self, key, value, subject):
        DeviceChannel.subject_update(self, key, value, subject)
        if self.connected and isinstance(key, tuple) and key[0] == self.channel:
            _, source, attribute = key
            group = self.source_groups[source]
            if attribute == ATTR_STREAM_READOUT:
                if value is not None:
                    self.get_value([group, attribute]).append(value)
                else:
                    self.set_value([group, attribute], [])
            else:
                self.set_value([group, attribute], value)

    def get_readout(self, source_group, attribute):
        if self.device.handle is None:
            return

        source_id = self.get_value([source_group, ATTR_ID])
        readout = si.GetValue_f64(self.device.handle, self.channel, source_id)
        self.set_value([source_group, attribute], readout)
        return readout

    def set_allow_streaming(self, source_index, value):
        si.SetProperty_i32(self.device.handle, si.EPK(si.Property.STREAMING_ENABLED, self.channel, source_index), value)
        max_fa = si.GetProperty_i32(self.device.handle, si.EPK(si.Property.MAX_FRAME_AGGREGATION, 0, 0))
        max_fr = si.GetProperty_i32(self.device.handle, si.EPK(si.Property.MAX_FRAME_RATE, 0, 0))
        self.device.set_attribute([GROUP_STREAMING, ATTR_FRAME_AGGREGATION, MAX], max_fa)
        self.device.set_attribute([GROUP_STREAMING, ATTR_FRAMERATE, MAX], max_fr)
        if value:
            self.device.stream_sources.append((self.channel, source_index))
        else:
            self.device.stream_sources.remove((self.channel, source_index))

    def poller_interval(self):
        for fun in self.polled_functions:
            try:
                fun()
            except si.bindings.Error:
                pass

    def start_polling(self):
        self.polling = True
        self.polled_functions = []
        for group in self.source_groups.values():
            self.polled_functions.append(
                lambda group=group: self.get_readout(group, ATTR_VALUE_READOUT)
            )
        self.polling_timer = PreciseCallbackTimer(300, self.poller_interval)
        self.polling_timer.start()

    def stop_polling(self):
        self.polling = False
        self.polling_timer.stop()
