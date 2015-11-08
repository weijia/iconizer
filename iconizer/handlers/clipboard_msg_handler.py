from iconizer.handlers.ui_msg_handler_base import UiMsgHandlerBase
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory

__author__ = 'weijia'


class ClipboardMsgHandler(UiMsgHandlerBase):
    def __init__(self, gui_factory):
        super(ClipboardMsgHandler, self).__init__()
        self.receivers = []
        self.gui_factory = gui_factory
        self.is_listening = False
        self.msg_service = MsgServiceFactory().get_msg_service()

    def is_listening_clipboard_event(self):
        return self.is_listening

    def handle(self, msg):
        if self.is_command(msg, "register_to_clipboard"):
            self.receivers.append(msg["target"])
            if not self.is_listening_clipboard_event():
                self.gui_factory.register_to_clipboard_event(self.on_clipboard_event)
                self.is_listening = True

    def on_clipboard_event(self):
        for receiver in self.receivers:
            try:
                data = self.gui_factory.get_clipboard_data()
                self.msg_service.send_to(receiver, {"msg_type": "clipboard", "data": {"text": data}})
            except:
                import traceback
                traceback.print_exc()

