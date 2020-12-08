from PyQt5 import QtWidgets
from views import AddHostDialog
from models import ConnectionData
import re


class AddHostDialogController(QtWidgets.QDialog):
    def __init__(self):
        super(AddHostDialogController, self).__init__()
        self.ui = AddHostDialog.Ui_AddHostDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.create_connection)
        self.connection = None

    def create_connection(self):
        host = self.ui.hostInput.text()
        if not re.match(r'([0-9]{1,3}\.)[0-9]{1,3}', host):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Wrong IP address')
            self.ui.hostInput.setText('')
            return
        username = self.ui.usernameInput.text()
        if not re.match(r'[0-9a-zA-Z]+', username):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Wrong username')
            self.ui.usernameInput.setText('')
            return
        password = self.ui.passwordInput.text()
        if len(password) < 1:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Wrong password')
            self.ui.passwordInput.setText('')
            return
        port = self.ui.portInput.text()
        if not re.match(r'[0-9]{1,5}', port):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Wrong port')
            self.ui.portInput.setText('')
            return
        else:
            port = int(port)
        self.connection = ConnectionData.ConnectionData(host, username, password, port)
        self.accept()

