from iconizer.console.drop_wnd_handler import DropWndHandler
# from iconizer.msg_service.auto_route_msg_service import AutoRouteMsgService
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory


class DropWndHandlerV2(DropWndHandler):
    def __init__(self, gui_factory):
        super(DropWndHandlerV2, self).__init__(gui_factory)
        self.msg_service = MsgServiceFactory().get_msg_service()
        self.wnd2target = {}
        self.target2wnd = {}

    def handle(self, msg):
        if msg["command"] == "DropWndV2":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        elif msg["command"] == "DestroyDropWndV2":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            # del self.target2wnd[msg]
            wnd.deleteLater()

    def drop_callback(self, drop_wnd, urls):
        # print "dropped: ", urls
        # print drop_wnd, self.wnd2target
        target = self.wnd2target[drop_wnd]
        # msg_service = AutoRouteMsgService()
        # msg_service.send_to(target, {"command": "dropped", "urls": urls})

        self.msg_service.send_to(target, {"command": "dropped", "urls": urls})
