from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QTreeWidget


class JuQTreeWidget(QTreeWidget):
    tree_copy = Signal()
    tree_paste = Signal()
    tree_del = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        pass
        # self.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.tree_copy.emit()
            print("tree_copy")
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            self.tree_paste.emit()
            print("tree_paste")
        # elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_X:
        #     self.s_cut.emit()
        elif event.key() == Qt.Key_Delete:
            print("tree_del")
            self.tree_del.emit()
