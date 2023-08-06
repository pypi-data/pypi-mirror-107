from socket import socket
from time import sleep
import threading




def sending():
   sock = socket()
   sock.connect(('localhost', 1337))
   count = 0
   sock.send(bytes(str(count), encoding='utf-8'))
   sleep(0.1)
   count = count + 1
   print("SEND COUNT", count)


a = [1,2]
for b in a:
   print('Поток:', b)
   threading.Thread(target=sending, args=()).start()
