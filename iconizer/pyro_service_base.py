import inspect
import logging
import os
import threading
import Pyro4
from services.svc_base.stoppableThread import StoppableThread

log = logging.getLogger(__name__)


class PyroServiceBase(StoppableThread):
    def __init__(self):
        super(PyroServiceBase, self).__init__()
        self.service_name = None
        self.uri = None
        self.pyro_daemon = None
        self.port = None

    def run(self):
        self.init_service_name()
        self.create_daemon()
        self.launch_service_msg_loop()

    def launch_service_msg_loop(self):
        if self.pyro_daemon is None:
            raise "Pyro daemon must be started first using create_daemon"
        #self.pyro_daemon.requestLoop(loopCondition=self.still_running)
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
        log.debug("Pyro service uri: "+str(self.uri))

    def register_to_name_server(self):
        if self.uri is None:
            raise "Pyro daemon must be started first using create_daemon"
        ns = Pyro4.locateNS()
        ns.register(self.service_name, self.uri)

    def still_running(self):
        print "still running"
        return True

    def pyro_shutdown(self):
        print 'shutting down daemon'
        self.pyro_daemon.shutdown()
        self.set_stop()
        print 'shutdown complete'

    def put_msg(self, msg):
        pass

    @staticmethod
    def get_file_basename(file_path):
        default_name = os.path.basename(file_path).replace(".py", "").replace(".exe", "")
        return default_name

    def get_filename(self):
        inspect_getouterframes = inspect.getouterframes(inspect.currentframe())
        frame, filename, line_number, function_name, lines, index = \
            inspect_getouterframes[3]
        (frame, filename, line_number, function_name, lines, index)
        return self.get_file_basename(filename)