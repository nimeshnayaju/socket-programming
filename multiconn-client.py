import socket
import selectors
import types
import sys

sel = selectors.DefaultSelector()

messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns): # A method to initiate connections
  server_addr = (host, port)
  for i in range(0, num_conns): # num_conns: number of connections to create to the server
    connid = i + 1
    print("Starting connection:", connid, "to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False) # Set the socket to non-blocking - calls made to this socket is no longer "block"
    sock.connect_ex(server_addr) # used instead of connect() because connect() would immediately raise a BlockingIOError exception. connect_ex() returns an error indicator, errno.EINPROGRESS, instead of raising an exxception while the connection is in process
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(connid=connid, msg_total=sum(len(m) for m in messages), recv_total=0, messages=list(messages), outb=b'') # Stores the socket data after the socket is set up and the messages the client will send to the server are copied to list(messages) since each connection will call socket.send() and modify the list
    sel.register(sock, events, data=data) # The information about what the client needs to send, has sent and received is stored in object data


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()