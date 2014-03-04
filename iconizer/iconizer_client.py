import Pyro4
from iconizer_consts import ICONIZER_SERVICE_NAME


class IconizerClient(object):
    def __init__(self):
        super(IconizerClient, self).__init__()
        self.launch_server = None

    def execute_in_remote(self, app_descriptor_dict):
        #try:
            self.get_launch_server().put_msg({"command": "launch", "apps": app_descriptor_dict})
        #except:
            #print "Calling remote execute, but server not running"

    def get_launch_server(self):
        if self.launch_server is None:
            uri_string = "PYRO:" + ICONIZER_SERVICE_NAME +\
                         "@127.0.0.1:8018"
            self.launch_server = Pyro4.Proxy(uri_string)
        return self.launch_server

    def is_running(self):
        self.get_launch_server().is_running()

    def register_to_name_server(self):
        self.get_launch_server().register_to_name_server()