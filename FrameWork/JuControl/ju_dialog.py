from PySide2.QtWidgets import QDialog
from qdarkstyle import load_stylesheet_pyside2


class JuDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setStyleSheet(load_stylesheet_pyside2())
        # self.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))
