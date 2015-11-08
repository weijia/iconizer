from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import InterfaceNotImplemented

__author__ = 'weijia'


# noinspection PyMethodMayBeStatic
class PyroReceiverBase(object):
    def put_msg(self):
        raise InterfaceNotImplemented

    def is_pyro_receiver(self):
        return True


class InvalidPyroReceiver(object):
    pass
