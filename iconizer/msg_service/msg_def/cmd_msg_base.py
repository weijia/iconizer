from UserDict import UserDict


class CmdMsgBase(UserDict):
    command = None
    msg_type = []

    def __init__(self, dict_param=None, **kwargs):
        UserDict.__init__(self, dict_param, **kwargs)
        self.set_cmd(self.command)

    def set_cmd(self, cmd):
        self.__setitem__("command", cmd)

    def set_msg_type(self, msg_type):
        self.__setitem__("msg_type", msg_type)

    def is_type(self, type_name):
        return self.get("msg_type", None) == type_name
