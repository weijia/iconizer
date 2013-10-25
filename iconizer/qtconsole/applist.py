import UserDict
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStandardItemModel, QStandardItem
from pyqt_console_output_wnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
from iconizer.qtconsole.notification import find_resource_in_pkg


class ListViewWindow(QtGui.QWidget, MinimizeOnClose, ToggleMaxMin):
    def __init__(self):
        super(ListViewWindow, self).__init__()
        #ui_full_path = findFileInProduct('app_list.ui')
        ui_full_path = find_resource_in_pkg('app_list.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.model = QStandardItemModel()

        self.listView.setModel(self.model)

        #self.show()
        self.listView.clicked.connect(self.item_clicked)
        self.minimized = True
        self.click_handler = None

    def item_clicked(self, index):
        if not (self.click_handler is None):
            self.click_handler(str(self.model.item(index.row()).text()))

    def set_click_handler(self, callback_func):
        self.click_handler = callback_func


class ItemToActionDictInListUi(UserDict.DictMixin):
    """
    Manage items in dict way. key is the item text, value is a dict: {"checked": True, "action": callback_func}
    callback_func will accept the key as param
    """
    def __init__(self):
        self.app_list = ListViewWindow()
        self.app_list.set_click_handler(self.item_click_callback)
        self.item_to_action_dict = {}
        self.item_dict = {}
        self.key2item = {}
        #self.app_list.show()

    def show_app_list(self):
        self.app_list.show()

    def new_item(self, key):
        item = QStandardItem(key)
        item.setCheckable(True)
        #item.setCheckable(value["checked"])
        self.app_list.model.appendRow(item)
        return item

    def __setitem__(self, key, value):
        #item = self.item_dict.get(key, self.new_item(key))

        if key in self.item_dict:
            item = self.key2item[key]
            #item.setCheckable(value["checked"])
        else:
            item = self.new_item(key)

        if value["checked"]:
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
        #print 'callback called:', str
        self.item_to_action_dict[str](str)