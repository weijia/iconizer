import Pyro4
from Pyro4.errors import NamingError
from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import MsgServiceProviderInterface, \
    UnknownReceiver
from iconizer.msg_service.pyro_msg_service.pyro_receiver import PyroReceiver
from iconizer.msg_service.pyro_msg_service.pyro_receiver_base import InvalidPyroReceiver
from iconizer.pyro_service_base import PyroServiceBase

__author__ = 'weijia'


# noinspection PyMethodMayBeStatic
class PyroMsgServiceProvider(MsgServiceProviderInterface):
    def __init__(self):
        super(PyroMsgServiceProvider, self).__init__()
        self.receiver_proxy_cache = {}
        self.listeners = []

    def send_to(self, receiver, msg):
        """
        Receiver is a string indicate the receiver's name, it may or may not contain protocol string to specify
        message sending protocol
        """
        proxy = self.get_receiver_proxy(receiver)
        # proxy._pyroOneway.add("put_msg")
        if proxy.is_pyro_receiver():
            proxy.put_msg(msg)
        else:
            raise InvalidPyroReceiver

    def create_msg_channel(self, channel_name, port=None):
        ch = PyroReceiver()
        ch.set_port(port)
        ch.set_service_name(channel_name)
        ch.start()
        return ch

    ########################
    # The following are internal functions
    ########################
    def get_receiver_proxy(self, receiver):
        if receiver in self.receiver_proxy_cache:
            proxy = self.receiver_proxy_cache.get(receiver)
        else:
            proxy = self.get_proxy_from_name_server(receiver)
            if proxy is None:
                proxy = self.get_proxy_from_name_directly(receiver)
            self.receiver_proxy_cache[receiver] = proxy
        return proxy

    def get_proxy_from_name_directly(self, receiver):
        if "PYRO:" in receiver:
            uri_string = receiver
        else:
            uri_string = "PYRO:" + receiver + \
                         "@localhost:8018"
        proxy = Pyro4.Proxy(uri_string)
        return proxy

    def get_proxy_from_name_server(self, receiver):
        # Locate NS
        try:
            ns = Pyro4.locateNS()
        except NamingError:
            return None
        # Find service name as receiver
        service_dict = ns.list()
        # Send to receiver by calling handle function of the service
        if receiver in service_dict:
            return Pyro4.Proxy(service_dict[receiver])
        else:
            print "unknown receiver:", receiver
            raise UnknownReceiver
