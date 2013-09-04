import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
from PyQt4.QtGui import QStandardItem
from PyQt4.QtCore import  Qt
from notification import Notification


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        #exitAction = self.menu.addAction("Exit")
        #exitAction.triggered.connect(self.exitHandler)
        self.setContextMenu(self.menu)
    #def exitHandler(self):
    #    QApplication.quit()
        
        
import UserDict
from applist import ApplicationList


class List2SystemTray(UserDict.DictMixin):
    def __init__(self, icon, parent=None):
        self.systemTrayIcon = SystemTrayIcon(icon, parent)
        self.systemTrayIcon.show()
        self.actionDict = {}
        #self.msg("App started")
        
    def __setitem__(self, key, value):
        action = self.systemTrayIcon.menu.addAction(key)
        action.triggered.connect(value)
        self.actionDict[key] = value

    def __delitem__(self, key):
        action = self.systemTrayIcon.menu.removeAction(key)
        #action.triggered.connect(value)
        action.triggerd.disconnect()
        del self.actionDict[key]
    
    def msg(self, msg):
        #self.systemTrayIcon.showMessage("Ufs system", msg, 20000)
        try:
            self.notification_window = Notification()
        except:
            import traceback
            traceback.print_exc()
        self.notification_window.noti(msg)
    

class ConsoleManager(UserDict.DictMixin):
    """
    Manage items in dict way. key is the item text, value is a dict: {"checked": True, "action": callback_func}
    callback_func will accept the key as param
    """
    def __init__(self):
        self.app_list = ApplicationList()
        self.app_list.set_click_handler(self.app_list_callback)
        self.actionDict = {}
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
        self.actionDict[key] = value["action"]
        self.item_dict[key] = value
        self.key2item[key] = item
        
    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise "not string"
        return self.key2item[key]
        
    def app_list_callback(self, str):
        #print 'callback called:', str
        self.actionDict[str](str)


def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    trayIcon = List2SystemTray(QtGui.QIcon("gf-16x16.png"), w)
    console_man = ConsoleManager()
    console_man["Good"] = {"checked": True, "action": None}
    trayIcon["Applications"] = console_man.show_app_list
    trayIcon["Exit"] = QtGui.QApplication.quit
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()