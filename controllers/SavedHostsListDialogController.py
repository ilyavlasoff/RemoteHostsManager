from PyQt5 import QtWidgets, QtGui, QtCore
from views import SavedHostsListDialog
import psycopg2
import os
import configparser
from models.ConnectionData import ConnectionData
from controllers.AddHostDialogController import AddHostDialogController


class SavedHostsListDialogController(QtWidgets.QDialog):
    def __init__(self):
        super(SavedHostsListDialogController, self).__init__()
        self.ui = SavedHostsListDialog.Ui_SavedHostsListDialog()
        self.ui.setupUi(self)
        self.ui.savedHostsList.setColumnCount(4)
        self.ui.savedHostsList.setHorizontalHeaderLabels(['Host', 'Username', 'Password', 'Port'])
        self.saved_connections = []
        self.chosen_connection = None
        self.update_hosts_list()

        self.ui.addButton.clicked.connect(self.add_new_host)
        self.ui.removeButton.clicked.connect(self.remove_host)
        self.ui.editButton.clicked.connect(self.edit_host)
        self.ui.connectButton.clicked.connect(self.choose_click)

    def choose_click(self):
        index = self.ui.savedHostsList.currentRow()
        if index < 0 or index > len(self.saved_connections):
            return
        self.chosen_connection = self.saved_connections[index]
        self.accept()

    def get_chosen_connection(self):
        return self.chosen_connection

    def add_new_host(self):
        add_new_host_dialog = AddHostDialogController()
        add_new_host_dialog.setModal(True)
        add_new_host_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if add_new_host_dialog.exec_() == QtWidgets.QDialog.Accepted:
            SavedHostsDBReader.add(add_new_host_dialog.connection)
            QtWidgets.QMessageBox.information(self, 'Success', 'Host was added successfully')
            self.update_hosts_list()

    def remove_host(self):
        index = self.ui.savedHostsList.currentRow()
        if index < 0 or index > len(self.saved_connections):
            return
        if QtWidgets.QMessageBox.question(self, 'Remove', 'This host will be removed permanently. Continue?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            SavedHostsDBReader.remove(self.saved_connections[index].get_id())
            QtWidgets.QMessageBox.information(self, 'Success', 'Host was removed successfully')
            self.update_hosts_list()

    def edit_host(self):
        index = self.ui.savedHostsList.currentRow()
        if index < 0 or index > len(self.saved_connections):
            return
        add_new_host_dialog = AddHostDialogController(self.saved_connections[index])
        add_new_host_dialog.setModal(True)
        add_new_host_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if add_new_host_dialog.exec_() == QtWidgets.QDialog.Accepted:
            SavedHostsDBReader.update(add_new_host_dialog.connection, self.saved_connections[index].get_id())
            QtWidgets.QMessageBox.information(self, 'Success', 'Host was edited successfully')
            self.update_hosts_list()

    def update_hosts_list(self):
        self.saved_connections = SavedHostsDBReader.read_all()
        self.ui.savedHostsList.clear()
        self.ui.savedHostsList.setRowCount(0)
        for conn in self.saved_connections:
            self.ui.savedHostsList.model().insertRow(self.ui.savedHostsList.rowCount())
            self.ui.savedHostsList.setItem(self.ui.savedHostsList.rowCount() - 1, 0,
                                           QtWidgets.QTableWidgetItem(conn.get_host()))
            self.ui.savedHostsList.setItem(self.ui.savedHostsList.rowCount() - 1, 1,
                                           QtWidgets.QTableWidgetItem(conn.get_username()))
            self.ui.savedHostsList.setItem(self.ui.savedHostsList.rowCount() - 1, 2,
                                           QtWidgets.QTableWidgetItem(conn.get_password()))
            self.ui.savedHostsList.setItem(self.ui.savedHostsList.rowCount() - 1, 3,
                                           QtWidgets.QTableWidgetItem(str(conn.get_port())))


class SavedHostsDBReader:
    connection = None

    @staticmethod
    def __connect():
        user, password, host, port, database = DatabaseConnectionConfigReader.read()
        SavedHostsDBReader.connection = psycopg2.connect(user=user,
                                                         password=password,
                                                         host=host,
                                                         port=port,
                                                         database=database)

    @staticmethod
    def read_all():
        if SavedHostsDBReader.connection is None:
            SavedHostsDBReader.__connect()
        cursor = SavedHostsDBReader.connection.cursor()
        cursor.execute('SELECT host, username, password, port, id FROM ssh_known_hosts;')
        records = cursor.fetchall()
        connection_data_array = []
        for record in records:
            conn_data = ConnectionData(record[0], record[1], record[2], record[3], record[4])
            connection_data_array.append(conn_data)
        return connection_data_array

    @staticmethod
    def add(connection_data):
        if SavedHostsDBReader.connection is None:
            SavedHostsDBReader.__connect()
        cursor = SavedHostsDBReader.connection.cursor()
        cursor.execute("INSERT INTO ssh_known_hosts(host, username, password, port) VALUES ('%s', '%s', '%s', '%s');" % (
            connection_data.get_host(), connection_data.get_username(), connection_data.get_password(),
            str(connection_data.get_port())
        ))
        SavedHostsDBReader.connection.commit()
        return

    @staticmethod
    def remove(index):
        if SavedHostsDBReader.connection is None:
            SavedHostsDBReader.__connect()
        cursor = SavedHostsDBReader.connection.cursor()
        cursor.execute('DELETE FROM ssh_known_hosts WHERE id=%s' % str(index))
        SavedHostsDBReader.connection.commit()
        return

    @staticmethod
    def update(connection_data, index):
        if SavedHostsDBReader.connection is None:
            SavedHostsDBReader.__connect()
        cursor = SavedHostsDBReader.connection.cursor()
        cursor.execute("UPDATE ssh_known_hosts SET host='%s', username='%s', password='%s', port=%s WHERE id=%s" % (
            connection_data.get_host(), connection_data.get_username(), connection_data.get_password(),
            str(connection_data.get_port()), str(index)
        ))
        SavedHostsDBReader.connection.commit()
        return

class DatabaseConnectionConfigReader:
    @staticmethod
    def read():
        confParser = configparser.RawConfigParser()
        config_path = os.path.abspath('dbconf.conf')
        confParser.read(config_path)
        user = confParser.get('dbconf', 'user')
        password = confParser.get('dbconf', 'password')
        host = confParser.get('dbconf', 'host')
        port = confParser.get('dbconf', 'port')
        database = confParser.get('dbconf', 'database')
        return user, password, host, port, database
