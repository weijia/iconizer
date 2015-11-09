from Queue import Queue
from iconizer.pyro_service_base import PyroServiceBase

__author__ = 'weijia'


class PyroReceiver(PyroServiceBase):
    def __init__(self):
        super(PyroReceiver, self).__init__()
        self.cached_msg = Queue()

    def put_msg(self, msg):
        self.cached_msg.put_nowait(msg)

    def get_msg(self):
        return self.cached_msg.get()
