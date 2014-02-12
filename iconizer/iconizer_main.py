#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import traceback
import Pyro4
from iconizer.console.launcher import CrossGuiLauncher, call_function_no_exception, call_callbacks_in_list_no_exception
from iconizer.nameserver import NameServerInThread
from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend

LAUNCHER = "ufs_launcher"
Pyro4.config.COMMTIMEOUT=0.5

class NameServerAlreadyStarted(Exception):
    pass


class Iconizer(threading.Thread):
    def __init__(self, log_dir=None, msg_service=None, python_executable=None):
        super(Iconizer, self).__init__()
        #self.launched_app_dict = {}
        self.launch_server = None
        #Create windows
        self.gui_launch_manger = None
        self.log_dir = log_dir
        self.msg_service = msg_service
        self.uri = None
        self.python_executable = python_executable

    #########################
    # Called through pyro only
    #########################
    def send_msg(self, msg):
        """
        Send command msg to GUI
        """
        print "sending msg:", msg
        self.get_gui_launch_manager().send_msg(msg)

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

    def add_final_close_listener(self, final_close_callback):
        self.get_gui_launch_manager().final_close_callback_list.append(final_close_callback)

    def add_close_listener(self, close_callback):
        self.get_gui_launch_manager().close_callback_list.append(close_callback)

    ######################
    # Internal functions
    ######################
    def get_gui_launch_manager(self):
        if self.gui_launch_manger is None:
            self.gui_launch_manger = CrossGuiLauncher(PyQtGuiBackend(), self.log_dir, self.msg_service, self.python_executable)
        return self.gui_launch_manger

    def start_gui_no_return(self, app_descriptor_dict={}):
        #Add closing callback, so when GUI was closing, Iconizer will got notified
        self.add_final_close_listener(self.on_final_close)

        #Start background thread running pyro service
        self.start()

        #Execute app must be called in the main thread
        call_function_no_exception(self.get_gui_launch_manager().execute_inconized, app_descriptor_dict)
        self.get_gui_launch_manager().start_cross_gui_launcher_no_return()

    def execute_in_remote(self, app_descriptor_dict):
        try:
            self.get_launch_server().send_msg({"command": "launch", "apps": app_descriptor_dict})
        except:
            print "Calling remote execute, but server not running"

    def launch_service_msg_loop(self):
        self.pyro_daemon = Pyro4.Daemon(port=8018)
        self.uri = self.pyro_daemon.register(self, LAUNCHER)
        self.pyro_daemon.requestLoop(loopCondition=self.still_running)

    def still_running(self):
        print "still running"

    def run(self):
        self.launch_service_msg_loop()

    def on_final_close(self):
        print 'shutting down daemon'
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
            uri_string = "PYRO:" + LAUNCHER +\
                         "@127.0.0.1:8018"
            self.launch_server = Pyro4.Proxy(uri_string)
        return self.launch_server


def main():
    Iconizer().execute({"test_app_id_for_later_killing": ["dir"]})


if __name__ == '__main__':
    main()