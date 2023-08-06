import socket
from time import sleep
serv = socket.socket()
serv.bind(('localhost', 1337))
serv.listen(10)
conn, addr = serv.accept()
print('WAITING DATA')
while True:
    data = conn.recv(1024)
    sleep(1)               # Имитируем выполнение операций
    print("DATA:", data.decode())