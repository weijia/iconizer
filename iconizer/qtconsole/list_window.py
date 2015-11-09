import UserDict
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStandardItemModel, QStandardItem
from pyqt_console_output_wnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
from iconizer.qtconsole.notification import find_resource_in_pkg


class ListViewWindow(QtGui.QWidget):
    def __init__(self):
        super(ListViewWindow, self).__init__()
        # ui_full_path = find_file_in_product('list_ui_widget.ui')
        ui_full_path = find_resource_in_pkg('list_window.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.model = QStandardItemModel()

        self.listView.setModel(self.model)

        # self.show()
        self.listView.clicked.connect(self.item_clicked)
        self.minimized = True
        self.click_handler = None

    def item_clicked(self, index):
        if not (self.click_handler is None):
            self.click_handler(str(self.model.item(index.row()).text()))

    def set_click_handler(self, callback_func):
        self.click_handler = callback_func


class ListDialog(ListViewWindow, MinimizeOnClose, ToggleMaxMin):
    pass


class ItemToActionDictInListUi(UserDict.DictMixin):
    """
    Manage items in dict way. key is the item text, value is a dict: {"checked": True, "action": callback_func}
    callback_func will accept the key as param
    """

    def __init__(self, list_window_class=ListDialog):
        self.ui_widget = list_window_class()
        self.ui_widget.set_click_handler(self.item_click_callback)
        self.item_to_action_dict = {}
        self.item_dict = {}
        self.key2item = {}
        # self.ui_widget.show()

    def show(self):
        self.ui_widget.show()

    def new_ui_item(self, key):
        ui_item = QStandardItem(key)
        ui_item.setCheckable(True)
        self.ui_widget.model.appendRow(ui_item)
        return ui_item

    def __setitem__(self, key, value):
        # item = self.item_dict.get(key, self.new_item(key))

        if key in self.item_dict:
            item = self.key2item[key]
        else:
            item = self.new_ui_item(key)

        if ("checked" in value) and (value["checked"]):
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.item_to_action_dict[key] = value["action"]
        self.item_dict[key] = value
        self.key2item[key] = item

    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise "not string"
        return self.key2item[key]

    def item_click_callback(self, str):
        # print 'callback called:', str
        self.item_to_action_dict[str](str)
