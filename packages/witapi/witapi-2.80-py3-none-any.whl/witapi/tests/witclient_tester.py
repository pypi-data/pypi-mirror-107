from witapi.main import WITClient
from witapi.tests import test_cfg
import time


if __name__ == '__main__':
    wclient = WITClient(test_cfg.internal_ip, test_cfg.port, test_cfg.login, test_cfg.pw)
    wclient.make_connection()
    response = wclient.make_auth()
    wclient.send_file(r'C:\Users\faizi\OneDrive\Рабочий стол\путевка моя.xlsx')
    """
    count = 0
    while True:
        count += 1
        wclient.send_data({'some':count})
        time.sleep(0.1)
    print(response)
    """
