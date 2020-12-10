from views.CustomListViewItem import CustomListViewItem
from PyQt5 import QtWidgets, QtGui, QtCore
from controllers.ChangeNameDialogController import ChangeNameDialogController
import asyncio
import os


class DataViewController:
    def __init__(self, cmd_executor, partition_view, fs_view):
        self.__partition_view = partition_view
        self.__fs_view = fs_view
        self.__cmd_executor = cmd_executor
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
            list_widget_data = CustomListViewItem(item.filesystem, item.mount_point, partition_image_path)
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
            current_item = self.__fs_view.currentItem()
            full_path = self.get_full_path(current_item)
            self.__cmd_executor.get_rm_command(full_path).execute()
            asyncio.ensure_future(self.catalog_list_update(current_item.parent()))

    def rename_item(self):
        rename_dialog = ChangeNameDialogController()
        rename_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if rename_dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_file_name = rename_dialog.get_filename()
            current_item = self.__fs_view.currentItem()
            old_full_path = self.get_full_path(current_item)
            new_full_path = old_full_path[:str.rfind(old_full_path, '/')] + '/' + new_file_name
            self.__cmd_executor.get_mv_command(old_full_path, new_full_path).execute()
            asyncio.ensure_future(self.catalog_list_update(current_item.parent()))

    def move_item(self):
        current_item = self.__fs_view.currentItem()
        full_path = self.get_full_path(current_item)

    def copy_item(self):
        pass

    def import_to_buffer(self):
        pass

    def export_from_buffer(self):
        pass

