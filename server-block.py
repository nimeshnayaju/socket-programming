import socket

s = socket.socket()

host = socket.gethostname()
port = 12345

s.bind((host, port))
s.listen(5)

while True:
  conn, addr = s.accept()

  data = conn.recv(1024)
  while data:
    print(data)
    data = conn.recv(1024)
  print("All data received")
  conn.close()
  break