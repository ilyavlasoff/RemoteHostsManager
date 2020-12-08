from controllers import MainWindowController
from PyQt5 import QtWidgets
import sys

qapp = QtWidgets.QApplication([])
application = MainWindowController.MainWindowController()
application.show()
sys.exit(qapp.exec())