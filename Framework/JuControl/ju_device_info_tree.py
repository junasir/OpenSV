
from copy import deepcopy
from PySide2.QtCore import QSize, Qt, Signal, QPoint
from PySide2.QtGui import QIcon, QMovie, QCursor
from PySide2.QtWidgets import (QComboBox, QTreeWidget, QTreeWidgetItem, QLabel)


class JuDevcieInfoWidget(QTreeWidget):
    device_move_event_signal = Signal(int, int)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setMouseTracking(True)
        # self.setFixedSize(400, 500)
        self._device_init_info = None
        self._device_index_map = None
        self._changed_vaild_flag = False
        self._set_ui()

    def device_info_show(self, device_init_info=None, device_index_map=None, init_flag=False):
        self._device_init_info = device_init_info
        self._device_index_map = {}
        self._set_ui(init_flag=init_flag)

    def _set_ui(self, init_flag=False):
        self.clear()
        if init_flag is True:
            self.setHeaderLabels(["Type", "Name", "Index", "", "", "Vendor", "Serial Num", "Label"])
            self.setColumnCount(8)
            self.hideColumn(2)
            self.hideColumn(3)
            self.hideColumn(4)
            self.hideColumn(5)
            self.hideColumn(6)
            self.hideColumn(7)
            self.setColumnWidth(0, 100)
            if type(self._device_init_info) is dict:
                for device_type, device_name in self._device_init_info.items():
                    if type(device_name) is list and type(device_type) is str and len(device_name) > 0:

                        device_index_items = []
                        for device_index in range(0, len(device_name)):
                            device_index_items.append(str(device_index + 1))
                        i = 0
                        one_device_index_map = {}
                        for one_device_name in device_name:
                            root_device_item = QTreeWidgetItem(self)
                            root_device_item.setText(0, device_type)
                            root_device_item.setText(1, one_device_name.get("name"))
                            cmb_device_index = QComboBox(self)
                            cmb_device_index.addItems(device_index_items)
                            root_device_item.setIcon(0, QIcon(u"./JuResource/img/ok.png"))
                            root_device_item.setText(3, str(i))
                            root_device_item.setText(4, str(i))
                            root_device_item.setText(5, str(one_device_name.get("vendor_name")))
                            root_device_item.setText(6, str(one_device_name.get("serial_num")))
                            self.addTopLevelItem(root_device_item)
                            cmb_device_index.setCurrentIndex(i)
                            cmb_device_index.currentIndexChanged.connect(self._device_index_changed)
                            self.setItemWidget(root_device_item, 2, cmb_device_index)
                            one_device_index_map[i] = i
                            i += 1
                        self._device_index_map[device_type] = deepcopy(one_device_index_map)
            if self.topLevelItemCount() == 0:
                self.setHeaderLabels(["Device Info"])
                self.setColumnCount(1)
                root_device_type = QTreeWidgetItem(self)
                root_device_type.setText(0, "No device found")
                root_device_type.setIcon(0, QIcon(u"./JuResource/img/error.png"))
        else:
            self.setHeaderLabels(["Device", "State"])
            self.setColumnCount(2)
            root_device_type = QTreeWidgetItem(self)
            root_device_type.setText(0, "Device loading...")
            movie = QMovie(u"JuResource/img/loading.gif")
            movie.setScaledSize(QSize(20, 20))
            label_loading = QLabel(self)
            label_loading.setMovie(movie)
            movie.start()
            self.setItemWidget(root_device_type, 1, label_loading)
            self.setColumnWidth(0, 200)

    def _device_index_changed(self, index=0):
        if self._changed_vaild_flag is False:
            self._changed_vaild_flag = True
            try:
                current_item = self.currentItem()
                current_item_index = int(current_item.text(4))
                # current_item_parent = current_item.parent()
                device_type = current_item.text(0)
                device_type_index = self._device_index_map.get(device_type)
                old_device_index = self._device_index_map.get(device_type, {}).get(current_item_index)
                for key, value in device_type_index.items():
                    if value == index:
                        self._device_index_map[device_type][key] = old_device_index
                        self._device_index_map[device_type][current_item_index] = index
                        same_type_item = self.findItems(device_type, Qt.MatchContains, 0)
                        same_index_item = self.findItems(str(key), Qt.MatchContains, 4)
                        for one_same_type_item in same_type_item:
                            for one_same_index_item in same_index_item:
                                if one_same_index_item is one_same_type_item:
                                    self.itemWidget(one_same_index_item, 2).setCurrentIndex(old_device_index)
                                    break
                        break
            except Exception:
                pass
                # print(e)
        self._changed_vaild_flag = False

    def get_device_map_tab(self):
        hardware_remap = {}
        for key, value in self._device_index_map.items():
            if type(value) is dict:
                hardware_remap[key] = {}
                for real_index, map_index in value.items():
                    hardware_remap[key][map_index] = real_index
        return hardware_remap

    def get_current_device_info(self):
        current_device_info = {}
        try:
            current_item = self.currentItem()
            current_device_info = {"type": current_item.text(0), "name": current_item.text(1),
                                   "index": int(current_item.text(4)), "Vendor": current_item.text(5),
                                   "serial_num": current_item.text(6)}

        except Exception:
            pass
        return deepcopy(current_device_info)

    def get_mouse(self):
        frame_y = self.parent().mapToGlobal(QPoint(0, 0)).y()
        mouse_y = QCursor().pos().y() - frame_y
        return mouse_y

    def mouseMoveEvent(self, evt):
        mouse_y = self.get_mouse()
        self.device_move_event_signal.emit(0, mouse_y - 70)

    def leaveEvent(self, evt):
        mouse_y = self.get_mouse()
        self.device_move_event_signal.emit(0, mouse_y - 70)

    def mouseReleaseEvent(self, evt):
        mouse_y = self.get_mouse()
        self.device_move_event_signal.emit(0, mouse_y - 70)
