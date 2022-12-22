from PyQt5.QtWidgets import QDialog
from .template.connection import Ui_Dialog
from random import randint
from utils.ip_adress import IpAddress


class ConnectDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.random_port_checkBox.stateChanged.connect(self.random_port)
        self.button_ok.clicked.connect(self.accept)
        self.client_port = None
        self.server = None

    def random_port(self, signal):
        if signal:
            self.port_edit.setDisabled(1)
            port = randint(1024, 65536)
            self.port_edit.setText(str(port))
        else:
            self.port_edit.setEnabled(1)

    @staticmethod
    def is_valid(client_port, server):
        message = ''
        if not (client_port.isdigit() and 1024 <= int(client_port) <= 65536):
            message = 'Некорректный порт клиента'
        elif server is None:
            message = 'Некорректный адресс сервера'
        return message

    def accept(self):
        client_port = self.port_edit.text()
        server_ip_port = self.ip_port_edit.text()
        server = IpAddress.parse_ip(server_ip_port)
        message = self.is_valid(client_port, server)
        if message:
            self.heading_label.setText(message)
        else:
            self.client_port = client_port
            self.server = server
            super().accept()
