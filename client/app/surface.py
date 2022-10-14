from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel
from time import time


class Surface(QLabel):
    def __init__(self, app):
        super().__init__()
        canvas = QtGui.QPixmap(2000, 2000)
        self.pen = QtGui.QPen()
        self.client = app.client
        self.setPixmap(canvas)
        self.painter = QtGui.QPainter(self.pixmap())
        self.set_pen()
        # self.setCursor(QCursor(QtCore.Qt.CrossCursor))

    def set_pen(self, size=5, color='red'):
        self.pen.setWidth(size)
        self.pen.setColor(QtGui.QColor(color))
        self.painter.setPen(self.pen)

    def set_message(self, position) -> str:
        point_info = {
                    "command": "draw",
                    "pen": {
                        "color": (self.pen.color().name()),
                        "width": self.pen.width()
                        },
                    "position": {
                        "x": position.x(),
                        "y": position.y()
                        },
                    "time": str(time())
                    }
        return str(point_info)

    def mouseMoveEvent(self, event):
        message = self.set_message(event)
        self.client.sendto(bytes(message, 'utf-8'), self.client.get_server)
        super().mouseMoveEvent(event)
