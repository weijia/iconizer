from PyQt4.QtGui import QStandardItemModel, QStandardItem
from PyQt4.QtCore import  Qt
from pyqt_console_output_wnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
import sys
from iconizer.qtconsole.notification import find_resource_in_pkg


class DroppableMain(QtGui.QMainWindow):
    def __init__(self):
        super(DroppableMain, self).__init__()
        self.show() 

def main():
    app = QtGui.QApplication(sys.argv)
    dropable = Droppable()
    main = DroppableMain()
    sys.exit(app.exec_())
    
#Codes got from http://stackoverflow.com/questions/7138773/draggable-window-with-pyqt4
class Draggable:
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

class Droppable(QtGui.QWidget, Draggable):

    def set_windows_flags(self):
        self.setWindowFlags(
            QtCore.Qt.CustomizeWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)

    def __init__(self, wnd_color = None):
        super(Droppable, self).__init__()
        ui_full_path = find_resource_in_pkg('droppable.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.set_windows_flags()
        self.setAcceptDrops(True)
        #print '-------------------------------------', g_config_dict["drop_wnd_color"]
        if not (wnd_color is None):
            #QtGui.QWidget.setBackground(self, QtGui.QColor(g_config_dict["drop_wnd_color"]))
            #self.setBackgroundRole(QtGui.QPalette.Dark);
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.red)
            self.setPalette(p)
            self.setAutoFillBackground(True)
        self.setGeometry(300,300,30,30)
        # The following is not working
        # self.setToolTip("hello world")
        self.show()
        self.drop_callback = None

    def dragEnterEvent(self, e):
        '''
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 
        '''
        e.accept()
        self.set_windows_flags()

    def set_drop_callback(self, drop_callback):
        self.drop_callback = drop_callback
        
    def dropEvent(self, e):
        print e.mimeData().urls()
        if self.drop_callback is None:
            return
        res = []
        for i in e.mimeData().urls():
            res.append(unicode(i.toString()))
        self.drop_callback(self, res)
        self.set_windows_flags()
        
if __name__ == '__main__':
    main()

