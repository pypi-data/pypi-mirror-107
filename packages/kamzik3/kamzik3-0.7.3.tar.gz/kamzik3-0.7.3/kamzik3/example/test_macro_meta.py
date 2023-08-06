import json
import zmq

# Host and port of Kamzik3 control socket
host = "127.0.0.1"
port = 60010

# Create socket
socket = zmq.Context.instance().socket(zmq.REQ)
socket.setsockopt(zmq.CONNECT_TIMEOUT, 1000)
socket.setsockopt(zmq.RCVTIMEO, 1000)
try:
    socket.connect("tcp://{}:{}".format(host, port))
    # Execute get_running_macros_meta method on MacroServer device
    socket.send_multipart([b"4", b"MacroServer", b"get_running_macros_meta", b"{}"], copy=False)

    # Receive response
    message = socket.recv_multipart()
    status, token, msg_type, output = message

    if status.decode():
        output = json.loads(output.decode())
    else:
        # Error in output, just return empty list - no running macro on Macro server
        output = []
except zmq.error.Again:
    # Connection error
    output = []

print(output)