from netmiko import ConnectHandler
from multiprocessing import Pool, Manager
import tqdm


def run_job(args):
    device, dictionary = args

    connection = ConnectHandler(**device)

    output = connection.send_command('show ip int b')
    dictionary[device['host']] = {'results': [output]}

    connection.disconnect()


if __name__ == '__main__':
    devices = [{'device_type': 'cisco_ios', 'host': '192.168.1.201', 'username': 'admin', 'password': 'Cisco123'},
               {'device_type': 'cisco_ios', 'host': '192.168.1.202', 'username': 'admin', 'password': 'Cisco123'},
               {'device_type': 'cisco_ios', 'host': '192.168.1.203', 'username': 'admin', 'password': 'Cisco123'}]
    manager = Manager()
    shared_dictionary = manager.dict()
    devices = [(i, shared_dictionary) for i in devices]
    pool = Pool(processes=7)
    for _ in tqdm.tqdm(pool.imap_unordered(run_job, devices), total=len(devices)):
        pass
    pool.close()
    pool.join()

    for k, v in shared_dictionary.items():
        print(f'Host: {k}')
        for o in v['results']:
            print(o)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
