# -*- coding: utf-8 -*-  
from pyqt_console_output_wnd import PyQtConsoleOutputWnd
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from pyqt_taskbar_icon import List2SystemTray, ConsoleManager
from PyQt4 import QtCore
import fileTools
from droppable import Droppable
from browser import Browser
from iconizer.console.gui_factory_base import GuiFactoryBase


class PyQtGuiBackend(QtCore.QObject, GuiFactoryBase):
    """
    We must inherit QObject to have pyqtSignal declared here. And QObject.__init__ should also be called.
    See http://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    """
    gui_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        super(PyQtGuiBackend, self).__init__()
        self.app = QtGui.QApplication(sys.argv)
        self.droppable_list = []
        self.browser_list = {}
        self.gui_signal.connect(self.msg_callback)
        self.gui_signal_callback = None

    ################################################
    #Msg related functions
    def trigger(self, msg):
        print "trigger called:", msg
        self.gui_signal.emit(msg)

    def set_msg_callback(self, callback):
        self.gui_signal_callback = callback

    def msg_callback(self, msg):
        if self.gui_signal_callback is None:
            return
        self.gui_signal_callback(msg)

    ################################################
    #GUI related
    def create_taskbar_icon_app(self):
        self.w = QtGui.QWidget()
        icon_full_path = fileTools.find_resource_in_pkg("gf-16x16.png")
        self.trayIcon = List2SystemTray(QtGui.QIcon(icon_full_path), self.w)
        #self.trayIcon["Example"] = exampleAction
        return self.trayIcon

    def create_console_output_wnd(self, parent, logFilePath=None):
        return PyQtConsoleOutputWnd(parent, logFilePath)

    def start_msg_loop(self):
        sys.exit(self.app.exec_())
        print "existing msg loop"

    def timeout(self, milliseconds, callback):
        self.ctimer = QtCore.QTimer()
        # constant timer
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), callback)
        self.ctimer.start(milliseconds)

    def exit(self):
        QtGui.QApplication.quit()

    def get_app_list(self):
        self.console_manager = ConsoleManager()
        return self.console_manager

    def create_drop_target(self, callback):
        drop_target_wnd = Droppable()
        self.droppable_list.append(drop_target_wnd)
        drop_target_wnd.set_drop_callback(callback)
        return drop_target_wnd

    def remove_browser(self, handle):
        if handle in self.browser_list:
            self.browser_list[handle].deleteLater()
            del self.browser_list[handle]

    def show_browser(self, handle, url):
        #when calling load, url will be quoted? Seems yes.
        if self.browser_list.has_key(handle):
            self.browser_list[handle].load(QUrl(url))
            self.browser_list[handle].show()
            self.browser_list[handle].raise_()
            self.browser_list[handle].activateWindow()
        else:
            web = Browser()
            web.load(QUrl(url))
            #print "pyqt opening: ", url
            #web.load(QUrl("http://baidu.com"))
            self.browser_list[handle] = web
            web.show()
            web.raise_()
            web.activateWindow()
            #objWebSettings = self.browser_list[handle].settings();
            #print objWebSettings.defaultTextEncoding();
            #print objWebSettings.fontFamily(0)
            #objWebSettings.setFontFamily(0, '����')
            #objWebSettings.setDefaultTextEncoding("gbk");

    def msg(self, msg):
        self.trayIcon.msg(msg)