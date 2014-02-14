#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Pyro4
from iconizer.iconizer_server import IconizerServer
from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend

LAUNCHER = "ufs_launcher"
Pyro4.config.COMMTIMEOUT=0.5

class NameServerAlreadyStarted(Exception):
    pass


class Iconizer(IconizerServer):
    ######################
    # External interface
    ######################
    def execute(self, app_descriptor_dict):
        if not self.is_server_already_started():
            self.start_gui_no_return(app_descriptor_dict)
        else:
            self.execute_in_remote(app_descriptor_dict)

    def execute_in_remote(self, app_descriptor_dict):
        try:
            self.get_launch_server().send_msg({"command": "launch", "apps": app_descriptor_dict})
        except:
            print "Calling remote execute, but server not running"

    def is_server_already_started(self):
        try:
            self.get_launch_server().is_running()
            print "Is running is True"
            return True
        except:
            print "Server not running"
            return False

    def get_launch_server(self):
        if self.launch_server is None:
            uri_string = "PYRO:" + LAUNCHER +\
                         "@127.0.0.1:8018"
            self.launch_server = Pyro4.Proxy(uri_string)
        return self.launch_server


def main():
    Iconizer().execute({"test_app_id_for_later_killing": ["dir"]})


if __name__ == '__main__':
    main()