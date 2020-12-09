from PyQt5 import QtWidgets, QtCore
from views import MainWindow
from controllers.ConnectionPropertiesDialogController import ConnectionPropertiesDialogController
from controllers.SavedHostsListDialogController import SavedHostsListDialogController
from services import SaverDataService
from core.ConnectionManager import ConnectionManager
from controllers.DataViewController import DataViewController


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_view()

        self.left_side_view_group = MainWindowViewGroup(self.ui.partitionsListWidgetLeft,
                                                          self.ui.catalogTreeWidgetLeft,
                                                          self.ui.connectionInfoLabelLeft, 'L', None)
        self.right_side_view_group = MainWindowViewGroup(self.ui.partitionsListWidgetRight,
                                                          self.ui.catalogTreeWidgetRight,
                                                          self.ui.connectionInfoLabelRight, 'R', None)
        self.setup_host_startup()

    def setup_host_startup(self):
        right_connection_info = self.load_state()
        left_connection_info = self.load_state()
        if left_connection_info is None:
            self.set_left_side_view_connection_properties()
        if right_connection_info is not None:
            self.connect_to_host(right_connection_info, self.right_side_view_group)

    def load_state(self):
        return SaverDataService.SaverDataService.load_state()
        #TODO: Loading saved configuration

    def setup_view(self):
        self.ui.actionRight_window_connection.setShortcut('Ctrl+R')
        self.ui.actionRight_window_connection.triggered.connect(self.set_right_side_view_connection_properties)

        self.ui.actionLeft_window_connection.setShortcut('Ctrl+L')
        self.ui.actionLeft_window_connection.triggered.connect(self.set_left_side_view_connection_properties)

        self.ui.actionSaved_hosts.setShortcut('Ctrl+H')
        self.ui.actionSaved_hosts.triggered.connect(self.manage_saved_hosts)

    def set_right_side_view_connection_properties(self):
        command_executor = self.manage_connection_properties(self.right_side_view_group.manager_key)
        self.connect_to_host(command_executor, self.right_side_view_group)

    def set_left_side_view_connection_properties(self):
        command_executor = self.manage_connection_properties(self.left_side_view_group.manager_key)
        self.connect_to_host(command_executor, self.left_side_view_group)

    def manage_saved_hosts(self):
        saved_hosts_manager = SavedHostsListDialogController()
        saved_hosts_manager.setModal(False)
        saved_hosts_manager.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        saved_hosts_manager.exec_()

    def manage_connection_properties(self, manager_key):
        connection_properties_dialog = ConnectionPropertiesDialogController(manager_key)
        connection_properties_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if connection_properties_dialog.exec_() == QtWidgets.QDialog.Accepted:
            return connection_properties_dialog.get_connection_executor()

    def connect_to_host(self, command_executor, view_group):
        if view_group.management_data_view is None:
            view_group.management_data_view = DataViewController(command_executor,
                                                      view_group.partition_widget,
                                                      view_group.catalog_widget)
        else:
            view_group.management_data_view.set_executor(command_executor)

    def create_command_executor(self, key, connection_data):
        return ConnectionManager.add_connection(key, connection_data).connect()


class MainWindowViewGroup:
    def __init__(self, partition_widget, catalog_widget, info_label, manager_key, data_view):
        self.partition_widget = partition_widget
        self.catalog_widget = catalog_widget
        self.info_label = info_label
        self.management_data_view = data_view
        self.manager_key = manager_key

