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
