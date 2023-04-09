from PySide2.QtGui import QPixmap, QIcon, QDrag
from PySide2.QtCore import QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QWidget, QPushButton, \
    QVBoxLayout, QSpacerItem, QSizePolicy
from nodeeditor.utils import dumpException


class QDMDragListbox(QWidget):
    def __init__(self, parent=None, auto_pack=None):
        super().__init__(parent)
        self.listwidget_all = {}
        self._Layout = QVBoxLayout(self)
        self._Layout.setContentsMargins(0, 0, 0, 0)
        self._Layout.setSpacing(0)
        self.widget = QWidget(self)
        self.one_verticalLayout = QVBoxLayout(self.widget)
        self.one_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.one_verticalLayout.setSpacing(0)
        self.auto_pack = auto_pack
        self.initUI()
        self._Layout.addWidget(self.widget)
        # ve_spac = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # # ve_spac.isEmpty()
        # self._Layout.addItem(ve_spac)
        # self._Layout.removeItem(ve_spac)

    def initUI(self):
        # init
        # self.setIconSize(QSize(32, 32))
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.setDragEnabled(True)
        #
        self.addMyItems()

    def addMyItems(self):

        CALC_NODES = self.auto_pack.CALC_NODES
        temp_test = {}
        for key, value in self.auto_pack.CALC_NODES_TYPE.items():
            temp = {}
            for i in value:
                temp[i] = CALC_NODES[i]
            temp_test[key] = temp
        for key, value in temp_test.items():
            self.new_item_list(key, value)

    def reconnect_item(self):
        CALC_NODES = self.auto_pack.CALC_NODES
        temp_test = {}
        for key, value in self.auto_pack.CALC_NODES_TYPE.items():
            temp = {}
            for i in value:
                temp[i] = CALC_NODES[i]
            temp_test[key] = temp
        for key, value in temp_test.items():
            if key in self.listwidget_all.keys():
                list_widget = self.listwidget_all[key]
                list_widget.clear()
                for item_key, item_value in value.items():
                    node = item_value
                    self.addMyItem(node.op_title, node.icon, node.op_code, one_list=list_widget)
            else:
                self.new_item_list(key, value)

    def new_item_list(self, key, value):
        one_widget = QWidget(self)
        one_verticalLayout = QVBoxLayout(one_widget)
        one_verticalLayout.setContentsMargins(0, 0, 0, 0)
        one_verticalLayout.setSpacing(0)
        pushbtn = QPushButton(one_widget)
        pushbtn.setText(key)
        one_verticalLayout.addWidget(pushbtn)
        one_list = MyListWidget(one_widget)
        one_list.setDragEnabled(True)
        one_list.isVisible()
        one_list.setVisible(True)
        # one_list.setFixedHeight(32 * len(value))
        one_verticalLayout.addWidget(one_list)
        self.listwidget_all[key] = one_list
        pushbtn.clicked.connect(lambda: self.push_button_click(one_list))
        for item_key, item_value in value.items():
            node = item_value
            self.addMyItem(node.op_title, node.icon, node.op_code, one_list=one_list)
        self.one_verticalLayout.addWidget(one_widget)

    def push_button_click(self, list):
        if list.isVisible():
            list.setVisible(False)
        else:
            list.setVisible(True)

    def addMyItem(self, name, icon=None, op_code=0, one_list=None):
        item = QListWidgetItem(name)  # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)
        one_list.addItem(item)


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super(MyListWidget, self).__init__(parent)
        self.LISTBOX_MIMETYPE = "application/x-item"

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeQString(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(self.LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)
