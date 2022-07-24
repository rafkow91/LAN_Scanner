import socket
import subprocess
from netifaces import interfaces, ifaddresses, AF_INET


class LAN_Scanner:
    def __init__(self, host_ip: str, subnet_mask: str, ports: tuple) -> None:
        self.host_ip = [int(x) for x in host_ip.split(
            '.')] if host_ip is not None else [192, 168, 1, 0]
        self.subnet_mask = [int(x) for x in subnet_mask.split(
            '.')] if subnet_mask is not None else [255, 255, 255, 0]
        self.ports = [int(x) for x in ports] if len(ports) != 0 else [80, 443, 8080, 22, 21]
        self.ips_in_subnet = []
        self.active_ips = []

    @staticmethod
    def _ping_ip(ip_addres: str) -> bool:
        response = subprocess.run(['ping', '-c', '1', ip_addres], capture_output=True)
        return not bool('0 received' in str(response.stdout).lower())

    @staticmethod
    def _check_open_ports(ip_address: str, ports: tuple = (80, 443)) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
            socket.setdefaulttimeout(1)

            for port in ports:
                result = socket_obj.connect_ex((ip_address, port))
                if result == 0:
                    return True

        return False

    def run(self) -> list:
        self._generate_ip_list()
        self._check_subnet()
        return self.active_ips

    def _check_ip(self, ip_address: str, ports: tuple = (80, 443)) -> bool:
        return any([
            self._check_open_ports(ip_address, ports),
            self._ping_ip(ip_address)
        ])

    def _check_subnet(self) -> None:
        for ip_address in self.ips_in_subnet:
            if ip_address is '.'.join([str(x) for x in self.host_ip]) or self._check_ip(ip_address, self.ports):
                self.active_ips.append(ip_address)

    def _generate_ip_list(self) -> None:
        available_ip_number = 2 ** self._subnet_mask_in_binary().count('0')

        multiplier = 0
        ip_range = (0, available_ip_number)

        while not(ip_range[0] <= self.host_ip[-1] <= ip_range[1]):
            multiplier += 1
            ip_range = (
                multiplier*available_ip_number,
                (multiplier+1)*available_ip_number
            )

        for i in range(ip_range[0]+1, ip_range[1]-1):
            ip_to_add = self.host_ip[:]
            ip_to_add[-1] = i
            self.ips_in_subnet.append('.'.join(
                [str(ip) for ip in ip_to_add]))

    def _subnet_mask_in_binary(self) -> str:
        return ''.join(['{:08b}'.format(x) for x in self.subnet_mask])


def check_interfaces() -> list:
    interfaces_list = []
    unserched = ['lo', 'vir', 'docker']

    for interface in interfaces():
        phisical_interface = True

        for text in unserched:
            if interface.find(text) != -1:
                phisical_interface = False
                break

        if phisical_interface:
            try:
                interfaces_list.append((
                    interface,
                    ifaddresses(interface)[AF_INET][0]['addr'],
                    ifaddresses(interface)[AF_INET][0]['netmask']
                ))
            except KeyError:
                pass

    return interfaces_list
