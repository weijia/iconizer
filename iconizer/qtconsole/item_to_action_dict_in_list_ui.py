import UserDict

import Qt
from PyQt4.QtGui import *
from list_dialog import ListDialog


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
            item.setCheckState(True)
        else:
            item.setCheckState(False)
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
