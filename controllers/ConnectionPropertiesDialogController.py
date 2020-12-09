from views.ConnectionPropertiesDialog import Ui_Dialog
from controllers.SavedHostsListDialogController import SavedHostsListDialogController
from PyQt5 import QtWidgets, QtCore
from core.ConnectionManager import ConnectionManager


class ConnectionPropertiesDialogController(QtWidgets.QDialog):
    def __init__(self, manager_key=None):
        super(ConnectionPropertiesDialogController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.manager_key = manager_key
        self.executor = None
        self.__update_status()

        self.ui.okButton.clicked.connect(self.__ok_clicked)
        self.ui.connectButton.clicked.connect(self.__connect_to_host)
        self.ui.disconnectButton.clicked.connect(self.__disconnect_from_host)

    def __update_status(self):
        managed_item = ConnectionManager.get_connection(self.manager_key)

        if not managed_item:
            self.ui.statusLine.setText('Disconnected')
            self.ui.usernameLine.setText('<Not stated>')
            self.ui.passwordLine.setText('<Not stated>')
            self.ui.hostLine.setText('<Not stated>')
            self.ui.portLine.setText('<Not stated>')
        else:
            self.ui.usernameLine.setText(managed_item.get_connection_data().get_username() or '')
            self.ui.passwordLine.setText(
                ''.join(['*' for _ in range(len(managed_item.get_connection_data().get_password()))]) or '')
            self.ui.hostLine.setText(managed_item.get_connection_data().get_host() or '')
            self.ui.portLine.setText(str(managed_item.get_connection_data().get_port()) or '')
            try:
                self.executor = managed_item.get_cmd_executor()
                self.ui.statusLine.setText('Connected')
            except Exception:
                self.ui.statusLine.setText('Disconnected')

    def __connect_to_host(self):
        saved_hosts_dialog = SavedHostsListDialogController()
        saved_hosts_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        saved_hosts_dialog.setModal(True)
        if saved_hosts_dialog.exec_() == QtWidgets.QDialog.Accepted:
            connection_data = saved_hosts_dialog.get_chosen_connection()
            conn = ConnectionManager.get_connection(self.manager_key)
            if not conn:
                conn = ConnectionManager.add_connection(self.manager_key, connection_data)
            conn.connect()
            self.__update_status()

    def __disconnect_from_host(self):
        pass

    def __ok_clicked(self):
        self.accept()

    def get_connection_executor(self):
        return self.executor
