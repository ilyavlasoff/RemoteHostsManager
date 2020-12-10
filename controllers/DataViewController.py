from views.CustomListViewItem import CustomListViewItem
from PyQt5 import QtWidgets, QtGui, QtCore
from controllers.ChangeNameDialogController import ChangeNameDialogController
import asyncio
import os
import random
import string


class DataViewController:
    def __init__(self, cmd_executor, partition_view, fs_view, neighbor):
        self.__partition_view = partition_view
        self.__fs_view = fs_view
        self.__cmd_executor = cmd_executor
        self.__neighbor = neighbor
        self.initial_views_update()

        def partition_changed_update_callback():
            asyncio.ensure_future(self.catalog_list_update())
        self.__partition_view.currentItemChanged.connect(partition_changed_update_callback)

        def catalog_list_update_callback(parent):
            asyncio.ensure_future(self.catalog_list_update(parent))
        self.__fs_view.itemExpanded.connect(catalog_list_update_callback)

        def catalog_clear_list(parent):
            asyncio.ensure_future(self.clear_dir_list(parent))
        self.__fs_view.itemCollapsed.connect(catalog_clear_list)
        self.__fs_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__fs_view.customContextMenuRequested[QtCore.QPoint].connect(self.on_context_menu)

    def get_executor(self):
        return self.__cmd_executor

    def set_executor(self, executor):
        self.__cmd_executor = executor
        self.initial_views_update()

    def initial_views_update(self):
        self.partitions_list_update()

    def partitions_list_update(self):
        df_cmd = self.__cmd_executor.get_df_command()
        df_data_list = df_cmd.execute()
        for item in df_data_list:
            partition_image_path = os.path.abspath('ui/media/partition_icon.png')
            info_string = 'Device: %s, size: %s, available: %s' % (item.filesystem, item.size, item.avail)
            list_widget_data = CustomListViewItem(info_string, item.mount_point, partition_image_path)
            list_widget_item = QtWidgets.QListWidgetItem(self.__partition_view)
            list_widget_item.setSizeHint(list_widget_data.sizeHint())
            self.__partition_view.addItem(list_widget_item)
            self.__partition_view.setItemWidget(list_widget_item, list_widget_data)

    def get_current_mount_point(self):
        selected_item = self.__partition_view.currentItem()
        item_widget = self.__partition_view.itemWidget(selected_item)
        mount_point = item_widget.textDownQLabel.text()
        if not mount_point:
            self.clear_dir_list()
            raise Exception('This partition is not mounted yet')
        return mount_point

    @asyncio.coroutine
    def clear_dir_list(self, parent=None):
        if parent is None:
            self.__fs_view.clear()
        else:
            if parent.childCount() > 2 or any(parent.child(i).childCount() > 1 for i in range(parent.childCount())):
                for i in reversed(range(parent.childCount())):
                    parent.removeChild(parent.child(i))
                parent.addChild(QtWidgets.QTreeWidgetItem(None, ['Loading...']))
        yield

    @asyncio.coroutine
    def catalog_list_update(self, parent=None):
        mount_point = self.get_current_mount_point()
        if parent is not None:
            full_dir_path = self.get_full_path(parent)
            for i in reversed(range(parent.childCount())):
                parent.removeChild(parent.child(i))
        else:
            yield from self.clear_dir_list(parent)
            full_dir_path = mount_point
        data = self.__cmd_executor.get_ls_command(full_dir_path).execute()
        for item in data:
            widget = QtWidgets.QTreeWidgetItem(None, [item.name, item.access_rights, item.created_at, item.owner, item.creator])
            if item.is_dir():
                widget.addChild(QtWidgets.QTreeWidgetItem(None, ['Loading...']))
            if parent:
                parent.addChild(widget)
            else:
                self.__fs_view.addTopLevelItem(widget)
        yield

    def get_full_path(self, item):
        current_dir = item
        prev_dirs = [item.text(0)]
        while current_dir.parent():
            current_dir = current_dir.parent()
            prev_dirs.append(current_dir.text(0))
        mount_point = self.get_current_mount_point()
        return mount_point + ('/' if mount_point[-1] != '/' else '') + '/'.join(reversed(prev_dirs))

    def on_context_menu(self):
        right_click_menu = QtWidgets.QMenu(self.__fs_view)

        rename_action = QtWidgets.QAction('Rename', self.__fs_view)
        rename_action.triggered.connect(self.rename_item)
        right_click_menu.addAction(rename_action)

        copy_action = QtWidgets.QAction('Copy', self.__fs_view)
        copy_action.triggered.connect(self.copy_item)
        right_click_menu.addAction(copy_action)

        move_action = QtWidgets.QAction('Move', self.__fs_view)
        move_action.triggered.connect(self.move_item)
        right_click_menu.addAction(move_action)

        remove_action = QtWidgets.QAction('Delete', self.__fs_view)
        remove_action.triggered.connect(self.delete_item)
        right_click_menu.addAction(remove_action)

        right_click_menu.exec_(QtGui.QCursor.pos())

    def delete_item(self, obj):
        if QtWidgets.QMessageBox.question(self.__fs_view, 'Delete', 'This file will be removed permanently. Continue?',
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            try:
                current_item = self.__fs_view.currentItem()
                full_path = self.get_full_path(current_item)
                self.__cmd_executor.get_rm_command(full_path).execute()
                asyncio.ensure_future(self.catalog_list_update(current_item.parent()))
            except Exception:
                QtWidgets.QMessageBox.critical(self.__fs_view, 'Error', 'Can not delete item')

    def rename_item(self):
        try:
            current_item = self.__fs_view.currentItem()
            rename_dialog = ChangeNameDialogController(current_item.text(0), 'Rename item')
            rename_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            if rename_dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_file_name = rename_dialog.get_filename()
                old_full_path = self.get_full_path(current_item)
                new_full_path = old_full_path[:str.rfind(old_full_path, '/')] + '/' + new_file_name
                self.__cmd_executor.get_mv_command(old_full_path, new_full_path).execute()
                asyncio.ensure_future(self.catalog_list_update(current_item.parent()))
        except Exception:
            QtWidgets.QMessageBox.critical(self.__fs_view, 'Error', 'Can not rename item')

    def move_item(self):
        self.copy_item(True)

    def copy_item(self, make_delete=False):
        try:
            if not self.__neighbor.management_data_view or type(
                    self.__neighbor.management_data_view) is not DataViewController:
                QtWidgets.QMessageBox.critical(self.__fs_view, 'Error', 'Can not make operation')
                return
            local_file_path = DataViewController.get_random_file_name()
            source_filename = self.import_to_buffer(local_file_path, make_delete)
            self.__neighbor.management_data_view.export_from_buffer(local_file_path, source_filename)
        except Exception:
            QtWidgets.QMessageBox.critical(self.__fs_view, 'Error', 'Can not copy or move item')

    def import_to_buffer(self, buffer_path, delete_remote):
        current_item = self.__fs_view.currentItem()
        filename = current_item.text(0)
        remote_file_path = self.get_full_path(current_item)
        self.__cmd_executor.get_import_command(remote_file_path, buffer_path, delete_remote).execute()
        return filename

    def export_from_buffer(self, buffer_path, destination_filename):
        current_item = self.__fs_view.currentItem()
        if not current_item:
            QtWidgets.QMessageBox.critical(self.__fs_view, 'Error', 'Destination not specified')
            return
        remote_file_path = self.get_full_path(current_item) + '/' + destination_filename
        self.__cmd_executor.get_export_command(buffer_path, remote_file_path).execute()
        if os.path.isdir(buffer_path):
            os.rmdir(buffer_path)
        elif os.path.isfile(buffer_path):
            os.remove(buffer_path)
        asyncio.ensure_future(self.catalog_list_update(current_item.parent()))

    @staticmethod
    def get_random_file_name():
        filename = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        return os.path.abspath('buffer/%s' % filename)


