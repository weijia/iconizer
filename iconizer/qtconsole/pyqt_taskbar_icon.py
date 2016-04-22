import sys
from PyQt4 import QtGui
from iconizer.qtconsole.list_window import ItemToActionDictInListUi
from notification import Notification
import UserDict


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        # exitAction = self.menu.addAction("Exit")
        # exitAction.triggered.connect(self.exitHandler)
        self.setContextMenu(self.menu)
        # def exitHandler(self):
        #    QApplication.quit()


class List2SystemTray(UserDict.DictMixin):
    def __init__(self, icon, parent=None):
        self.system_tray_icon = SystemTrayIcon(icon, parent)
        self.system_tray_icon.show()
        self.item_to_action_dict = {}
        # self.msg("App started")
        self.notification_window = None

    def __setitem__(self, key, value):
        action = self.system_tray_icon.menu.addAction(key)
        action.triggered.connect(value)
        self.item_to_action_dict[key] = value

    def __delitem__(self, key):
        action = self.system_tray_icon.menu.removeAction(key)
        # action.triggered.connect(value)
        action.triggerd.disconnect()
        del self.item_to_action_dict[key]

    def msg(self, msg):
        # self.system_tray_icon.showMessage("Ufs system", msg, 20000)
        try:
            self.notification_window = Notification()
        except:
            import traceback

            traceback.print_exc()
        self.notification_window.noti(msg)


def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    tray_icon = List2SystemTray(QtGui.QIcon("gf-16x16.png"), w)
    console_man = ItemToActionDictInListUi()
    console_man["Good"] = {"checked": True, "action": None}
    tray_icon["Applications"] = console_man.show
    tray_icon["Exit"] = QtGui.QApplication.quit
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
