class LAN_Scanner:
    def __init__(self, host_ip: str, subnet_mask: str, ports: tuple) -> None:
        self.hostname = [int(x) for x in host_ip.split(
            '.')] if host_ip is not None else [192, 168, 1, 0]
        self.subnet_mask = [int(x) for x in subnet_mask.split(
            '.')] if subnet_mask is not None else [255, 255, 255, 0]
        self.ports = [int(x) for x in ports] if len(ports) != 0 else [80, 443, 8080, 22, 21]
        self.ips_in_subnet = []

    def _subnet_mask_in_binary(self) -> str:
        return ''.join(['{:08b}'.format(x) for x in self.subnet_mask])

    def _generate_ip_list(self) -> list:
        available_ip_number = 2 ** self._subnet_mask_in_binary().count('0') - 2
        if available_ip_number == 254:
            for i in range(1, 255):
                ip_to_add = 0
        return available_ip_number