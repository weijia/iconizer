from PyQt4.QtGui import QStandardItemModel
from pyqt_console_output_wnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
from iconizer.qtconsole.notification import findFileInProduct


class ApplicationList(QtGui.QWidget, MinimizeOnClose, ToggleMaxMin):
    def __init__(self):
        super(ApplicationList, self).__init__()
        ui_full_path = findFileInProduct('app_list.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.model = QStandardItemModel()

        self.listView.setModel(self.model)

        #self.show()
        self.listView.clicked.connect(self.item_clicked)
        self.minimized = True

    def item_clicked(self, index):
        self.click_handler(str(self.model.item(index.row()).text()))

    def set_click_handler(self, callback_func):
        self.click_handler = callback_func
