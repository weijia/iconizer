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
        self._mouse_button = None
        self.listView.setModel(self.model)

        # self.show()
        self.listView.clicked.connect(self.item_clicked)
        # self.listView.doubleClicked.connect(self.handle_right_click)
        self.minimized = True
        self.click_handler = None
        self.right_click_handler = None
        self.list_view_mouse_pressed = self.listView.mousePressEvent
        self.listView.mousePressEvent = self.mousePressEvent
    #     self.ui.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    #     self.ui.connect(self.ui, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
    #                                      self.on_context)
    #
    # def on_context(self, point):
    #     # Create a menu
    #     menu = QtGui.QMenu("Menu", self)
    #     menu.addAction(self.mAction1)
    #     menu.addAction(self.mAction2)
    #     # Show the context menu.
    #     menu.exec_(self.view.mapToGlobal(point))

    def item_clicked(self, index):
        row_text = str(self.model.item(index.row()).text())
        # mouse_buttons = QtGui.qApp.mouseButtons()
        # print int(mouse_buttons)
        if self._mouse_button == QtCore.Qt.RightButton:
            if self.right_click_handler:
                self.right_click_handler(row_text)
        elif not (self.click_handler is None):
            self.click_handler(row_text)

    # def handle_right_click(self, index):
    #     row_text = str(self.model.item(index.row()).text())
    #     if self.right_click_handler:
    #         self.right_click_handler(row_text)

    def set_click_handler(self, callback_func):
        self.click_handler = callback_func

    def mousePressEvent(self, event):
        self._mouse_button = event.button()
        self.list_view_mouse_pressed(event)
        # self.item_clicked()


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
        self.ui_widget.right_click_handler = self.right_click_handler
        self.item_to_action_dict = {}
        self.item_right_click_action = {}
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
        self.item_right_click_action[key] = value.get("on_right_click", None)
        self.item_dict[key] = value
        self.key2item[key] = item

    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise "not string"
        return self.key2item[key]

    def item_click_callback(self, str):
        # print 'callback called:', str
        self.item_to_action_dict[str](str)

    def right_click_handler(self, str):
        if self.item_right_click_action[str]:
            self.item_right_click_action[str](str)

    def __delitem__(self, key):
        item = self.key2item[key]
        self.ui_widget.model.removeRow(item.row())
        del self.item_to_action_dict[key]
        del self.item_right_click_action[key]
        del self.item_dict[key]
        del self.key2item[key]
