import sys
from PyQt5 import QtGui, QtWidgets


class CustomListViewItem(QtWidgets.QWidget):
    def __init__(self, text_up, text_down, icon_path, parent=None):
        super(CustomListViewItem, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        self.textUpQLabel.setText(text_up)
        self.textDownQLabel.setText(text_down)
        self.iconQLabel.setPixmap(QtGui.QPixmap(icon_path))

    def set_text_up(self, text):
        self.textUpQLabel.setText(text)

    def set_text_down(self, text):
        self.textDownQLabel.setText(text)

    def set_icon(self, path_to_image):
        self.iconQLabel.setPixmap(QtGui.QPixmap(path_to_image))
