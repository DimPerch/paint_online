import socketserver
from utils.ip_adress import IpAddress
from json import loads
SERVER_ADDRESS = IpAddress('192.168.26.133', 8888)


class ServerHandler(socketserver.BaseRequestHandler):
    connection_list = []

    def handle(self):
        data, socket = self.request
        json_data = loads(data.decode('utf-8').replace("\'", "\""))
        if json_data['command'] == 'hello' and self.client_address not in self.connection_list:
            self.connection_list.append(self.client_address)
            print('Connected by', self.client_address)
        elif json_data['command'] == 'buy':
            self.connection_list.remove(self.client_address)
            print('Disconnected by', self.client_address)

        for client in self.connection_list:
            try:
                socket.sendto(data, client)
            except ConnectionError:
                print(f'Client {client} suddenly closed, cannot send')


if __name__ == '__main__':
    with socketserver.UDPServer(SERVER_ADDRESS.to_tuple(), ServerHandler) as server:
        print(f'Server run on {SERVER_ADDRESS}')
        server.serve_forever()
