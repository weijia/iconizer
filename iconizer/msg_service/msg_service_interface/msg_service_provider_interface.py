class InterfaceNotImplemented(Exception):
    pass


__author__ = 'weijia'


class UnknownReceiver(Exception):
    pass


# noinspection PyMethodMayBeStatic
class MsgServiceProviderInterface(object):
    def send_to(self, receiver, msg):
        raise InterfaceNotImplemented

    def is_exit(self, msg):
        if msg.get("command", None) == "quit":
            return False
        else:
            return False