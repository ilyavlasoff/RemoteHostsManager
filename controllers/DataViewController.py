from views.CustomListViewItem import CustomListViewItem
from PyQt5 import QtWidgets
import asyncio


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
            list_widget_data = CustomListViewItem(item.filesystem, item.mount_point, '../ui/media/partition_icon.png')
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
            for i in reversed(range(self.__fs_view.topLevelItemCount())):
                item = self.__fs_view.takeTopLevelItem(i)
                del item
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
            current_dir = parent
            prev_dirs = [parent.text(0)]
            while current_dir.parent():
                current_dir = current_dir.parent()
                prev_dirs.append(current_dir.text(0))
            full_dir_path = mount_point + '/' + '/'.join(reversed(prev_dirs))
            for i in reversed(range(parent.childCount())):
                parent.removeChild(parent.child(i))
        else:
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


