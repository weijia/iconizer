from PyQt4.QtGui import QApplication, QTextBrowser
from PyQt4 import QtCore
import sys

from iconizer.console.console_output_collector import decode_str


class ConsoleOutputWndBase(object):
    def set_title(self):
        pass


class MinimizeOnClose(object):
    # The closeEvent function is a standard event handler for QT to process close button in the window
    def closeEvent(self, event):
        # print "close event captured. Do nothing.", event
        # "minimize"
        self.hide()
        event.ignore()
        self.minimized = True
        if hasattr(self, "parent"):
            if hasattr(self.parent, "on_child_closed"):
                self.parent.on_child_closed(self)


class ToggleMaxMin(object):

    def toggle(self):
        if not hasattr(self, 'minimized'):
            self.minimized = True
        if self.minimized:
            self.show()
            self.minimized = False
        else:
            self.hide()
            self.minimized = True
        return self.minimized


class PyQtConsoleOutputWnd(QTextBrowser, MinimizeOnClose, ToggleMaxMin):
    log_updated_signal = QtCore.pyqtSignal(object)
    # signal_registered = False

    """
    This class manages console windows, it will kill applications for every console window.
    """

    def __init__(self, parent, log_file_path=None):
        # self.browser.setDocumentTitle('dsds')
        super(PyQtConsoleOutputWnd, self).__init__()
        # self.show()
        # if not self.signal_registered:
        self.log_updated_signal.connect(self.update_view)
        # signal_registered = True
        self.parent = parent
        '''
        self.isMinimized = True
        self.window.hide()
        self.kept_text = ''
        self.stopped = False
        '''
        if log_file_path is None:
            self.log_file = None
        else:
            self.log_file = open(log_file_path, 'w')

    def set_title(self, title):
        self.setWindowTitle(title)

    def on_close_clicked(self, widget):
        self.parent.console_wnd_close_clicked(self)
        # self.isMinimized = True
        # self.window.hide()
        # return False

    def update_view_callback(self, data):
        self.log_updated_signal.emit(data.replace('\r\n', '\n'))

    def update_view(self, data):
        # print "updateView:", data
        if not (self.log_file is None):
            decode_str(data)
            encoded_data = data.encode(sys.getdefaultencoding(), 'replace')
            self.log_file.write(encoded_data)
        for line in data.split("\n")[0:-1]:
            self.append(line)

    '''
    def closeEvent(self,event):
        # Let the Exit button handle tab closing
        print "close event captured. Do nothing.", event
        #"minimize"
        self.hide()
        event.ignore()
    '''
    '''
    def set_title(self, title):
        self.window.set_title(title)

    def updateView(self, data):
        #print "updateView:", data
        if not (self.logFile is None):
            self.logFile.write(data)
        if not self.isMinimized:
            self.realUpdateView(data)
        else:
            self.kept_text += data
            if len(self.kept_text) > MAX_DISPLAY_TEXT_NUM:
                previous_line_n = self.kept_text.rfind("\n", MAX_DISPLAY_TEXT_NUM)
                previous_line_r = self.kept_text.rfind("\r", MAX_DISPLAY_TEXT_NUM)
                previous_line_end = max([previous_line_n, previous_line_r])
                self.kept_text = self.kept_text[previous_line_end+1:]
                    
            
    def realUpdateView(self, data):
        buf = self.textview.get_buffer()
        line_count = buf.get_line_count()
        if line_count >= MAX_DISPLAYED_LINE_NUM:
            #Remove some lines
            line_number = line_count - REMOVE_LINE_NUMBER
            iter = buf.get_iter_at_line(line_number)
            startIter = buf.get_iter_at_offset(0)
            buf.delete(startIter, iter)
        buf.insert(buf.get_end_iter(), data)
        
    def show(self, *args):
        cl('show called')
        if not self.isMinimized:
            return
        buf = self.textview.get_buffer()
        buf.set_text("")
        buf.insert(buf.get_end_iter(), self.kept_text)
        self.kept_text = ''
        self.isMinimized = False
        self.window.show(*args)
        
    def min(self, data):
        ncl('min called')
        buf = self.textview.get_buffer()
        #False means do not get hidden text
        self.kept_text = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        self.isMinimized = True
        self.window.hide()
        
    def topMost(self, widget):
        self.topMostFlag = not self.topMostFlag
        self.window.set_keep_above(self.topMostFlag)
    '''
