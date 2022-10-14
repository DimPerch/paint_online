from threading import Thread
from json import loads

from PyQt5.QtCore import QPoint


class Listener(Thread):
    def __init__(self, app_object):
        super().__init__()
        self.app = app_object
        self.last_draw = None
        self.is_listen = False

    def input_message(self, message):
        str_data = message.decode('utf-8').replace("\'", "\"")
        data = loads(str_data)
        if data['command'] == 'draw':
            if self.last_draw and float(data['time']) - float(self.last_draw['time']) <= 0.1:
                self.app.surface.painter.drawLine(QPoint(self.last_draw['position']['x'],
                                                         self.last_draw['position']['y']),
                                                  QPoint(data['position']['x'],
                                                         data['position']['y']))
            else:
                self.app.surface.painter.drawPoint(QPoint(data['position']['x'], data['position']['y']))

            self.last_draw = data
            self.app.surface.update()
        if data['command'] == 'bye':
            self.close()

    def listen(self):
        while self.is_listen:
            input_data = self.app.client.recv(1024)
            self.input_message(input_data)

    def run(self):
        self.is_listen = True
        try:
            self.listen()
        except KeyboardInterrupt:
            print(f'client {self.app.client.client_address} was stopped')
