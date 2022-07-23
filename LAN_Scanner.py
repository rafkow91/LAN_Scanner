import socket
import subprocess

import click


@click.command()
@click.option('-i', '--ip', 'hostname', help='Network IP address')
@click.option('-m', '--subnet_mask', help='Subnet mask')
@click.option('-p', '--ports', help='Checked ports', multiple=True)
def check_ip(hostname, subnet_mask, ports) -> bool:
    hostname2 = [int(x) for x in hostname.split('.')] if hostname is not None else [192, 168, 1, 0]
    subnet_mask2 = [int(x) for x in subnet_mask.split('.')] if subnet_mask is not None else [255, 255, 255, 0]
    ports2 = [int(x) for x in ports] if len(ports) != 0 else [80, 443, 8080, 22, 21]
    # response = subprocess.run(['ping', '-c', '1', hostname], capture_output=True)
    # ping_response = str(response.stdout).lower()
    print(hostname2, subnet_mask2, ports2)

    # if 'unreachable' in ping_response:
    #     print(True)
    #     return True
    # elif 'unreachable' not in ping_response:
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
    #         socket.setdefaulttimeout(1)
    #         for port in ports:
    #             result = socket_obj.connect_ex((hostname, port))
    #             if result == 0:
    #                 print(True)
    #                 return True

    # print(False)
    # return False


if __name__ == '__main__':
    print(check_ip())
