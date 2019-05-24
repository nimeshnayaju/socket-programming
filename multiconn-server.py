# https://realpython.com/python-sockets/

import socket
import selectors
import types
import sys

sel = selectors.DefaultSelector()

def accept_wrapper(sock): # A function to get the new object and register it with selector
  conn, addr = sock.accept()
  print("Accepted connection from:", addr)
  conn.setblocking(False) # Set the socket to non-blocking - calls made to this socket is no longer "block"
  data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") # Stores the socket data after the socket is set up
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  sel.register(conn, events, data=data)
  
def service_connection(key, mask):
  sock = key.fileobj
  data = key.data
  if mask & selectors.EVENT_READ:
    recv_data = sock.recv(1024)
    if recv_data:
      data.outb += recv_data
    else: # "block" if no data is received
      print("Closing connection to:", data.addr)
      sel.unregister(sock)
      sock.close() # Close the server socket since the client socket is closed
  if mask & selectors.EVENT_WRITE:
    if data.outb:
      print("Echoing", repr(data.outb), "to", data.addr)
      sent = sock.send(data.outb) # Echoes received data stored in data.outb to client
      data.outb = data.outb[sent:] # The bytes are then removed from the send buffer


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port)) # Binds the IP socket to a local address
lsock.listen() # Enables a server to accept connections
print('Listening on:', (host, port))
lsock.setblocking(False) # Set the socket to non-blocking - calls made to this socket is no longer "block"
sel.register(lsock, selectors.EVENT_READ, data=None) # Registers the socket to be monitored with sel.select()

try:
    # Set up an event loop
    while True:
      events = sel.select(timeout=None) # "blocks" until there are sockets ready for I/O; returns a list of (key, events) tuples, one for each socket
      for key, mask in events:
        if key.data is None: # Accept the connection because its from a listening socket
          accept_wrapper(key.fileobj) # key.fileobj is the socket object
        else: # Service the connection since it's a client socket that's already been accepted
          service_connection(key, mask) # mask is an event mask of the operations that are ready
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()