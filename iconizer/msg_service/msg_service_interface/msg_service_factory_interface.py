from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import InterfaceNotImplemented
from iconizer.msg_service.pyro_msg_service.pyro_msg_service_provider import PyroMsgServiceProvider

__author__ = 'weijia'


# noinspection PyMethodMayBeStatic
class MsgServiceFactoryInterface(object):
    def get_msg_service(self):
        raise InterfaceNotImplemented


class MsgServiceFactory(MsgServiceFactoryInterface):
    def get_msg_service(self):
        return PyroMsgServiceProvider()
