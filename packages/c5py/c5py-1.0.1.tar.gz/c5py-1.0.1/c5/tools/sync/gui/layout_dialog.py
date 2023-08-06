from PyQt5.QtWidgets import QWidget, QDialog
from layoutEditorUi import Ui_LayoutDialog

class LayoutDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_LayoutDialog()
        self.ui.setupUi(self)
        self.ui.preview.selectionChanged.connect(self.selection_changed)

    def selection_changed(self, container_name):
        print(container_name)
