import socket

sock = socket.socket()
host = socket.gethostname()
sock.connect((host, 12345))
sock.setblocking(0)

data = b'Hello World'
assert sock.send(data)