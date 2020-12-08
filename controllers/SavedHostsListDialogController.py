from PyQt5 import QtWidgets
from views import SavedHostsListDialog


class SavedHostsListDialogController(QtWidgets.QDialog):
    def __init__(self):
        super(SavedHostsListDialogController, self).__init__()
        self.ui = SavedHostsListDialog.Ui_SavedHostsListDialog()
        self.ui.setupUi(self)
