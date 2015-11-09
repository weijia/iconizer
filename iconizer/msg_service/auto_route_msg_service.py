import logging
from predefined_receivers import TAGGING_RECEIVER


log = logging.getLogger(__name__)


class AutoRouteMsgService(MsgServiceInterface):
    def __init__(self):
        super(AutoRouteMsgService, self).__init__()
        self.pyro_msg_service = PyroMsgService()

    def send_to(self, receiver, msg):
        try:
            self.pyro_msg_service.send_to(receiver, msg)
        except UnknownReceiver:
            print "Unknown receiver:", receiver
            log.error("Unknown receiver:"+receiver)

    def send_tagging_msg(self, msg):
        try:
            self.pyro_msg_service.send_to(TAGGING_RECEIVER, msg)
        except UnknownReceiver:
            pass