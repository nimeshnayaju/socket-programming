#https://realpython.com/python-sockets/

import socket

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-priviledged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Uses socket.SOCK_STREAM as the socket type to set up a Tranmission Control Protocol (TCP)
  s.bind((HOST, PORT)) # Binds the IP socket to a local address
  s.listen() # Enables a server to accept connections
  conn, addr = s.accept() # Wait for an incoming connection and return the new socket represeting the connection and the address of the client

  with conn:
    print('Client Address:', addr)
    while True:
      data = conn.recv(1024) # Receive upto 1024 buffersize bytes from the socket
      if not data:
        break # Close the connection is an empty bytes object is returned
      conn.sendall(data) # Send a data string to the socket

