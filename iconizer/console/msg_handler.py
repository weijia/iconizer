
class GuiServiceMsgHandler(object):
    def __init__(self, launcher):
        super(GuiServiceMsgHandler, self).__init__()
        self.launcher = launcher
        self.gui_factory = launcher.gui_factory
        self.wnd2target = {}
        self.target2wnd = {}
        self.handle2browser = {}

    def handle_msg(self, msg):
        if msg["command"] == "Launch":
            self.launcher.execute_inconized(msg["apps"])
        elif msg["command"] == "DropWnd":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        elif msg["command"] == "DestroyDropWnd":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            #del self.target2wnd[msg]
            wnd.deleteLater()
        elif msg["command"] == "Browser":
            url = msg["url"]
            handle = msg["handle"]
            self.gui_factory.show_browser(handle, url)
        elif msg["command"] == "DestroyBrowser":
            handle = msg["handle"]
            self.gui_factory.remove_browser(handle)
        elif msg["command"] == "notify":
            msg_str = msg["msg"]
            self.gui_factory.msg(msg_str)