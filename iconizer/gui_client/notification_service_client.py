from iconizer.gui_client.msg_service_client import MsgServiceClient
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME


class NotificationServiceClient(MsgServiceClient):
    def notify(self, msg):
        self.ufs_msg_service.send_to(ICONIZER_SERVICE_NAME, {"command": "notify", "msg": msg})