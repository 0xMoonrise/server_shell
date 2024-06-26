import socket
import fcntl
import struct
import json


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


def print_shells(shells):
    return '\n'.join([f"\tType: {k}\t Shell: {v}" for k, v in shells.items()])
