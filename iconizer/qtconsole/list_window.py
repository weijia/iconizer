import UserDict
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStandardItemModel, QStandardItem
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
