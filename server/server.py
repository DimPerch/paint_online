import socketserver


SERVER_ADDRESS = ('localhost', 8888)


class ServerHandler(socketserver.BaseRequestHandler):
    connection_list = []

    def handle(self):
        data, socket = self.request

        if self.client_address not in self.connection_list:
            self.connection_list.append(self.client_address)
            print('Connected by', self.client_address)

        for client in self.connection_list:
            try:
                socket.sendto(data.upper(), client)
            except ConnectionError:
                print(f'Client {client} suddenly closed, cannot send')


if __name__ == '__main__':
    with socketserver.UDPServer(SERVER_ADDRESS, ServerHandler) as server:
        server.serve_forever()
