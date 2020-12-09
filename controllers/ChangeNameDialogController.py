from views.ChangeNameDialog import Ui_Dialog
from PyQt5 import QtWidgets


class ChangeNameDialogController(QtWidgets.QDialog):
    def __init__(self, old_name=None, title_label=None):
        super(ChangeNameDialogController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        if old_name is not None:
            self.ui.filenameLineEdit.setText(old_name)
        if title_label is not None:
            self.ui.optionLabel.setText(title_label)
        self.filename = None
        self.ui.buttonBox.accepted.connect(self.filename_ready)

    def filename_ready(self):
        self.filename = self.ui.filenameLineEdit.text()

    def get_filename(self):
        return self.filename
