class InterfaceNotImplemented(Exception):
    pass


__author__ = 'weijia'


class UnknownReceiver(Exception):
    pass


# noinspection PyMethodMayBeStatic
class MsgServiceProviderInterface(object):
    def send_to(self, receiver, msg):
        raise InterfaceNotImplemented
