import re


class IpAddress:
    def __init__(self, ip: str, port: int):
        if ip.lower() == 'localhost':
            ip = '127.0.0.1'
        self.ip = str(ip)
        self.port = str(port)

    @staticmethod
    def is_valid(ip, port) -> bool:
        pattern = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
        return pattern.match(ip) and port.isdigit() and 0 <= int(port) <= 65535

    @staticmethod
    def parse_ip(ip_str):
        if ip_str.count(':') == 1:
            ip_str = ip_str.replace(' ', '')
            ip, port = ip_str.split(':')
            if IpAddress.is_valid(ip, port):
                return IpAddress(ip, port)

    @property
    def get_ip(self) -> str:
        return self.ip

    @property
    def get_port(self) -> str:
        return self.port

    def to_tuple(self) -> tuple:
        return self.ip, int(self.port)

    def __str__(self):
        return f'{self.ip}:{self.port}'
