import time

from iconizer.msg_service.msg_def.cmd_msg_base import CmdMsgBase


class FileUrlListMsg(CmdMsgBase):
    def set_file_url_list(self, urls):
        self.__setitem__("urls", urls)

    def get_file_url_list(self):
        return self.__getitem__("urls")


class DropTargetRegMsg(CmdMsgBase):
    command = "DropWndV2"


class DropEventMsg(FileUrlListMsg):
    command = "drop"
    msg_type = "drop"


class DelayedMsg(CmdMsgBase):
    command = "delayed_pull_request"


class TagEnumeratorMsg(CmdMsgBase):
    command = "tag_enumerator_msg"


class FolderChangeNotification(CmdMsgBase):
    command = "folder_change"


def send_delayed_msg(channel, delay_seconds=5):
    time.sleep(delay_seconds)
    channel.put_msg(DelayedMsg())
