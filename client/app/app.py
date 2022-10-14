from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QSlider
from template.window import Ui_MainWindow
from connect_dialog import ConnectDialog
from surface import Surface
from client import Client
from listener import Listener


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_pencil.clicked.connect(self.show_dialog_color)
        self.button_connect.clicked.connect(self.show_dialog_connect)

        self.client = None
        self.surface = None
        self.listener = None

    def show_dialog_color(self):
        dialog = QColorDialog()
        pen_size = QSlider(Qt.Horizontal)
        pen_size.setMinimum(1)
        pen_size.setMaximum(6)
        layout = dialog.layout()
        layout.addWidget(pen_size)
        dialog.setLayout(layout)
        if dialog.exec_() and self.surface:
            self.surface.set_pen(size=pen_size.value(), color=dialog.selectedColor().name())

    def show_dialog_connect(self):
        dialog = ConnectDialog()
        if dialog.exec_():
            ip = Client.get_client_address(dialog.client_port)
            self.connect(dialog.server, ip)

    def connect(self, server_address, client_address):
        print(server_address, client_address)
        self.client = Client(client_address.to_tuple(), server_address.to_tuple())
        self.surface = Surface(self)
        self.listener = Listener(self)
        self.scrollArea.setWidget(self.surface)
        self.client.sendto(bytes(str({"command": "hello"}), 'utf-8'), self.client.get_server)
        self.listener.start()

    def closeEvent(self, event):
        if self.client:
            self.client.sendto(bytes(str({"command": "buy"}), 'utf-8'), self.client.get_server)
            self.client.sendto(bytes(str({"command": "buy"}), 'utf-8'), self.client.get_ip)
        if self.listener:
            self.listener.is_listen = False
        event.accept()
