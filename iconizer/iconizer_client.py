import logging
import Pyro4
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory
from iconizer_consts import ICONIZER_SERVICE_NAME

log = logging.getLogger(__name__)


class IconizerClient(object):
    def __init__(self):
        super(IconizerClient, self).__init__()
        self.launch_server = None
        self.msg_service = None

    def execute_in_remote(self, app_descriptor_dict):
        """
        Start an task in remote
        :param app_descriptor_dict: {"task name", ["app full path", "param1", "param2"]}
        :return:
        """
        self.init_msg_service()
        self.msg_service.send_to(ICONIZER_SERVICE_NAME, {"command": "launch", "apps": app_descriptor_dict})

        # # try:
        # self.get_launch_server().put_msg({"command": "launch", "apps": app_descriptor_dict})
        # # except:
        # #   print "Calling remote execute, but server not running"

    def init_msg_service(self):
        if self.msg_service is None:
            self.msg_service = MsgServiceFactory().get_msg_service()

    def get_launch_server(self):
        log.debug("Getting server")
        # if self.launch_server is None:
        #     uri_string = "PYRO:" + ICONIZER_SERVICE_NAME + \
        #                  "@localhost:8018"
        #     self.launch_server = Pyro4.Proxy(uri_string)
        # return self.launch_server
        self.init_msg_service()
        return self.msg_service.get_receiver_proxy(ICONIZER_SERVICE_NAME)

    def is_running(self):
        return self.get_launch_server().is_running()

    def register_to_name_server(self):
        self.get_launch_server().register_to_name_server()
