import threading
import Pyro4


class NameServerInThread(threading.Thread):
    def __init__(self):
        super(NameServerInThread, self).__init__()
        self.name_server_daemon = None

    @staticmethod
    def is_name_server_started():
        try:
            ns = Pyro4.locateNS()
            return True
        except:
            return False

    def name_server_msg_loop(self):
        nsUri, daemon, bcserver = Pyro4.naming.startNS()
        self.name_server_daemon = daemon
        print nsUri, daemon, bcserver
        try:
            daemon.requestLoop()
        except:
            import traceback
            traceback.print_exc()
        finally:
            daemon.close()
            if bcserver is not None:
                bcserver.close()

    def run(self):
        if self.is_name_server_started():
            raise "Name server running"

        self.name_server_msg_loop()
        print("NS shut down.")

    def shutdown(self):
        self.name_server_daemon.shutdown()
