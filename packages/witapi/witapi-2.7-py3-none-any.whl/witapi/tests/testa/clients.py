from socket import socket
from time import sleep
sock = socket()
sock.connect(('localhost', 1337))
count = 0
while True:
   sock.send(bytes(str(count), encoding='utf-8'))
   sleep(0.1)
   count = count + 1
   print("SEND COUNT", count)