import threading
import Pyro4


class PyroServiceObj(threading.Thread):
    def __init__(self, service_name):
        super(PyroServiceObj, self).__init__()
        self.service_name = service_name
        self.uri = None
        self.pyro_daemon = None

    def run(self):
        self.launch_service_msg_loop()

    def launch_service_msg_loop(self):
        if self.pyro_daemon is None:
            self.pyro_daemon = Pyro4.Daemon(port=8018)
            self.uri = self.pyro_daemon.register(self, self.service_name)
            print self.uri
            #self.pyro_daemon.requestLoop(loopCondition=self.still_running)
            self.pyro_daemon.requestLoop()

    def still_running(self):
        print "still running"
        return True

    def pyro_shutdown(self):
        print 'shutting down daemon'
        self.pyro_daemon.shutdown()
        print 'shutdown complete'

    def register_to_name_server(self):
        ns = Pyro4.locateNS()
        ns.register(self.service_name, self.uri)