import socket
from time import sleep
import threading


SERVER_ADDRESS = ('localhost', 8888)
CLIENT_ADDRESS = ('localhost', 4422)


class Client:
    def __init__(self, address: tuple, server: tuple):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(address)
        self.server = server

        self.listener = Listener(self.client)
        self.listener.start()
        self.loop_sender()

    def loop_sender(self):
        """Only for demo console using"""
        while True:
            output_data = input('Enter data: ')
            self.client.sendto(bytes(output_data, 'utf-8'), self.server)


class Listener(threading.Thread):
    def __init__(self, client_obj: Client):
        super().__init__()
        self.client = client_obj

    def listen(self):
        while True:
            input_data = self.client.recv(1024)
            print(f'Received: {input_data}')

    def run(self):
        try:
            self.listen()
        except KeyboardInterrupt:
            print(f'client {self.client.client_address} was stopped')


if __name__ == '__main__':
    client = Client(CLIENT_ADDRESS, SERVER_ADDRESS)
