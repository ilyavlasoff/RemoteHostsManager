from PyQt5 import QtWidgets, QtCore
from views import MainWindow
from controllers import SavedHostsListDialogController, AddHostDialogController
from services import SaverDataService
from core.ConnectionManager import ConnectionManager
from controllers.DataViewController import DataViewController


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.data_view = None
        self.setup_view()
        self.setup_host_startup()

    def setup_view(self):
        self.ui.actionSaved_hosts.setShortcut('Ctrl+H')
        self.ui.actionSaved_hosts.setToolTip('List of previously saved hosts')
        self.ui.actionSaved_hosts.triggered.connect(self.show_saved_hosts_list)

        self.ui.actionConnect_to.setShortcut('Ctrl+O')
        self.ui.actionConnect_to.setToolTip('Connect to specified host')
        self.ui.actionConnect_to.triggered.connect(self.connect_to_host)

    def setup_host_startup(self):
        remoted_host = self.load_state()
        if remoted_host is None:
            remoted_host = self.get_connection_data()
        self.connect_to_host(remoted_host)

    def show_saved_hosts_list(self):
        hosts_dialog = SavedHostsListDialogController.SavedHostsListDialogController()
        hosts_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if hosts_dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def get_connection_data(self):
        connection_dialog = AddHostDialogController.AddHostDialogController()
        connection_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if connection_dialog.exec_() == QtWidgets.QDialog.Accepted:
            return connection_dialog.connection

    def load_state(self):
        return SaverDataService.SaverDataService.load_state()

    def connect_to_host(self, remoted_host):
        try:
            command_executor = ConnectionManager.connect(remoted_host)
        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Error while connecting to host', QtWidgets.QMessageBox.Ok)
            return
        if self.data_view is None:
            self.data_view = DataViewController(command_executor, self.ui.partitionsListWidget, self.ui.catalogTreeWidget)
        else:
            self.data_view.set_executor(command_executor)

