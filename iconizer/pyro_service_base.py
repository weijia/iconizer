from Queue import Queue
import inspect
import logging
import os
import Pyro4
from iconizer.msg_service.pyro_msg_service.pyro_receiver_base import PyroReceiverBase
from stoppable_thread import StoppableThread

log = logging.getLogger(__name__)


class PyroServiceBase(PyroReceiverBase, StoppableThread):
    def __init__(self):
        super(PyroServiceBase, self).__init__()
        self.service_name = None
        self.uri = None
        self.pyro_daemon = None
        self.port = None
        self.start_queue = Queue()

    def set_port(self, port):
        self.port = port

    def run(self):
        self.init_service_name()
        self.create_daemon()
        self.start_queue.put("start")
        self.launch_service_msg_loop()

    def launch_service_msg_loop(self):
        if self.pyro_daemon is None:
            raise "Pyro daemon must be started first using create_daemon"
        # self.pyro_daemon.requestLoop(loopCondition=self.still_running)
        self.pyro_daemon.requestLoop()

    def start_daemon_register_and_launch_loop(self):
        self.init_service_name()
        self.create_daemon()
        self.register_to_name_server()
        self.launch_service_msg_loop()

    def set_service_name(self, service_name):
        self.service_name = service_name

    def init_service_name(self):
        if self.service_name is None:
            self.service_name = self.get_filename()

    def get_service_name(self):
        return self.service_name

    def create_daemon(self):
        if self.service_name is None:
            raise "Service name not set"
        if self.port is None:
            self.pyro_daemon = Pyro4.Daemon()
        else:
            self.pyro_daemon = Pyro4.Daemon(port=self.port)
        self.uri = self.pyro_daemon.register(self, self.service_name)
        log.debug("Pyro service uri: " + str(self.uri))
        print("Pyro service uri: " + str(self.uri))

    def get_channel_full_name(self):
        print self.uri
        return str(self.uri)

    def register_to_name_server(self):
        if self.uri is None:
            raise "Pyro daemon must be started first using create_daemon"
        ns = Pyro4.locateNS()
        log.debug("Registering ", self.service_name)
        print "Registering ", self.service_name
        ns.register(self.service_name, self.uri)

    # noinspection PyMethodMayBeStatic
    def still_running(self):
        print "still running"
        return True

    def pyro_shutdown(self):
        print 'shutting down daemon'
        self.pyro_daemon.shutdown()
        self.set_stop()
        print 'shutdown complete'

    def get_filename(self):
        inspect_getouterframes = inspect.getouterframes(inspect.currentframe())
        frame, filename, line_number, function_name, lines, index = \
            inspect_getouterframes[4]
        (frame, filename, line_number, function_name, lines, index)
        return self.get_file_basename(filename)

    def wait_for_channel_start(self):
        self.start_queue.get()
