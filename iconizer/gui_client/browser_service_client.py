from iconizer.gui_client.msg_service_client import MsgServiceClient
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME

__author__ = 'weijia'


class BrowserServiceClass(MsgServiceClient):
    def open_browser(self, url, browser_handle="tagging"):
        self.ufs_msg_service.send_to(ICONIZER_SERVICE_NAME,
                                     {"command": "Browser",
                                      "url": url,
                                      "handle": browser_handle}
                                     )
