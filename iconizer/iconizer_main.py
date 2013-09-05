#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import Pyro4
from iconizer.console.launcher import CrossGuiLauncher
from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend


class Iconizer(threading.Thread):
    def __init__(self):
        super(Iconizer, self).__init__()
        self.launched_app_dict = {}
        self.launch_server = None

    #########################
    # Called through pyro only
    #########################
    def send_msg(self, msg):
        """
        Send command msg to GUI
        """
        print "sending msg:", msg
        self.gui_launch_manger.send_msg(msg)

    def is_running(self):
        return True

    ######################
    # External interface
    ######################
    def execute(self, app_descriptor_dict):
        if not self.is_server_already_started():
            self.start_gui_no_return(app_descriptor_dict)
        else:
            self.execute_in_remote(app_descriptor_dict)

    ######################
    # Internal functions
    ######################
    def start_gui_no_return(self, app_descriptor_dict={}):
        self.app_descriptor_dict = app_descriptor_dict
        #Create windows
        self.gui_launch_manger = CrossGuiLauncher(PyQtGuiBackend())
        #Add closing callback, so when GUI was closing, Iconizer will got notified
        self.gui_launch_manger.add_final_close_listener(self.on_close)

        #Start background thread running pyro service
        self.start()

        #Execute app must be called in the main thread
        try:
            self.gui_launch_manger.execute_inconized(self.app_descriptor_dict)
        except:
            pass
        self.gui_launch_manger.start_cross_gui_launcher_no_return()

    def execute_in_remote(self, app_descriptor_dict):
        try:
            self.get_launch_server().send_msg({"command": "launch", "apps": app_descriptor_dict})
        except:
            print "Calling remote execute, but server not running"

    def run(self):
        self.pyro_daemon = Pyro4.Daemon(port=8018)
        uri = self.pyro_daemon.register(self, "ufs_launcher")
        print "uri=", uri
        #self.pyro_daemon.requestLoop(loopCondition=lambda: not self.must_shutdown)
        #Pyro4.config.COMMTIMEOUT=3.5
        self.pyro_daemon.requestLoop()

    def on_close(self):
        self.pyro_daemon.shutdown()

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
            uri_string = "PYRO:ufs_launcher@127.0.0.1:8018"
            self.launch_server = Pyro4.Proxy(uri_string)
        return self.launch_server


def main():
    Iconizer().execute({"testapp_id_for_later_killing": ["dir"]})


if __name__ == '__main__':
    main()