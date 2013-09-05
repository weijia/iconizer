from pyqt_console_output_wnd import ToggleMaxMin, MinimizeOnClose
from PyQt4.QtWebKit import *

class Browser(QWebView, ToggleMaxMin, MinimizeOnClose):
    pass