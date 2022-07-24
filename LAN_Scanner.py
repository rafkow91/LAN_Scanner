import click

from utils import LAN_Scanner, check_interfaces

# TODO: trzeba cały program zrefaktorować !!!


@click.command()
@click.option('-i', '--ip', 'hostname', help='Network IP address')
@click.option('-m', '--subnet_mask', help='Subnet mask')
@click.option('-p', '--ports', help='Checked ports', multiple=True)
def main(hostname, subnet_mask, ports) -> bool:
    if hostname is None and subnet_mask is None:
        interfaces_list = check_interfaces()
    else:
        interfaces_list = [('my_check', hostname, subnet_mask)]

    for interface in interfaces_list:
        scanner = LAN_Scanner(interface[1], interface[2], ports)
        results = scanner.run()
        print(f'Interface: {interface[0]}\t(IP: {interface[1]})\nActive ips in network:')
        for result in results:
            print(result)
        print('-' * 15)


if __name__ == '__main__':
    main()
