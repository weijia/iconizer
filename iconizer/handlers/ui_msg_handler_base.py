from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import InterfaceNotImplemented

__author__ = 'weijia'


class UiMsgHandlerBase(object):
    COMMAND_NAME_PROP = "command"

    def handle(self, msg):
        raise InterfaceNotImplemented

    def is_command(self, msg, command_name):
        return msg[self.COMMAND_NAME_PROP] == command_name
