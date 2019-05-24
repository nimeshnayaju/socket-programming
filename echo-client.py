# https://realpython.com/python-sockets/

import socket

HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 65432 # The port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Uses socket.SOCK_STREAM as the socket type to set up a Tranmission Control Protocol (TCP)
  s.connect((HOST, PORT)) # Connect the socket to a remote address
  s.sendall(b'Hello, world') # Send a data string to the socket
  data = s.recv(1024) # Read server's reply

print("Data string received:", repr(data)) # returns canonical string representation of object