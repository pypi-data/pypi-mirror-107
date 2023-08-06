from witapi.main import WITClient
from witapi.tests import test_cfg
import time
import threading


def connect_thread():
    wclient = WITClient(test_cfg.internal_ip, test_cfg.port, test_cfg.login, test_cfg.pw)
    wclient.make_connection()
    response = wclient.make_auth()
    wclient.send_file(r'C:\Users\faizi\OneDrive\Рабочий стол\путевка моя.xlsx')

if __name__ == '__main__':
    clients = [1,2]
    for client in clients:
        print('Starting', client)
        threading.Thread(target=connect_thread, args=()).start()
        print('sleeping')
        time.sleep(5)

