import socket
from utils.ip_adress import IpAddress


class Client(socket.socket):
    def __init__(self, address: tuple, server: tuple):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(address)
        self._ip = address
        self._server = server
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @staticmethod
    def get_client_address(port):
        ip = socket.gethostbyname(socket.gethostname())
        return IpAddress(ip, port)

    @property
    def get_ip(self):
        return self._ip

    @property
    def get_server(self):
        return self._server
