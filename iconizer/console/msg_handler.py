from iconizer.console.drop_wnd_handler import DropWndHandler
from iconizer.console.drop_wnd_handler_v2 import DropWndHandlerV2
from iconizer.handlers.clipboard_msg_handler import ClipboardMsgHandler
from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import InterfaceNotImplemented


class GuiServiceMsgHandler(object):
    def __init__(self, gui_launch_manger):
        super(GuiServiceMsgHandler, self).__init__()
        self.gui_launch_manger = gui_launch_manger
        self.gui_factory = gui_launch_manger.gui_factory
        self.wnd2target = {}
        self.target2wnd = {}
        self.handle2browser = {}
        self.drop_wnd_cmd_handler = DropWndHandler(self.gui_factory)
        self.drop_wnd_cmd_handler_v2 = DropWndHandlerV2(self.gui_factory)
        self.clipboard_cmd_handler = ClipboardMsgHandler(self.gui_factory)
        self.extra_handler = {"DropWnd": self.drop_wnd_cmd_handler,
                              "DestroyDropWnd": self.drop_wnd_cmd_handler,
                              "DropWndV2": self.drop_wnd_cmd_handler_v2,
                              "DestroyDropWndV2": self.drop_wnd_cmd_handler_v2,
                              "register_to_clipboard": self.clipboard_cmd_handler,
                              }

    def handle_msg(self, msg):
        command = msg["command"]
        if command == "launch":
            print "apps: ", msg["apps"]
            self.gui_launch_manger.execute_iconized(msg["apps"])
        elif command == "Browser":
            url = msg["url"]
            handle = msg["handle"]
            self.gui_factory.show_browser(handle, url)
        elif command == "DestroyBrowser":
            handle = msg["handle"]
            self.gui_factory.remove_browser(handle)
        elif command == "notify":
            msg_str = msg["msg"]
            self.gui_factory.msg(msg_str)
        else:
            if command in self.extra_handler:
                self.extra_handler[command].handle(msg)