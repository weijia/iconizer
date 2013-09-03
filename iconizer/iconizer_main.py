#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import Pyro4
from iconizer.console.launcher import CrossGuiLauncher
from iconizer.qtconsole.PyQtGuiFactory import PyQtGuiFactory


class Iconizer(threading.Thread):
    def __init__(self):
        super(Iconizer, self).__init__()
        self.launched_app_dict = {}

    def start_gui(self):
        self.launcher = CrossGuiLauncher(PyQtGuiFactory())
        self.launcher.add_close_listener(self.on_close)
        self.start()
        self.launcher.start_cross_gui_launcher_no_return()

    def run(self):
        self.pyro_daemon = Pyro4.Daemon(port=8018)
        uri = self.pyro_daemon.register(self)
        print "uri=", uri
        #self.pyro_daemon.requestLoop(loopCondition=lambda: not self.must_shutdown)
        #Pyro4.config.COMMTIMEOUT=3.5
        self.pyro_daemon.requestLoop()

    def on_close(self):
        self.pyro_daemon.shutdown()

    '''
    def launch(self, app_descriptor_dict):
        self.send_launch_request(app_descriptor_dict)
    '''

    def execute(self, app_descriptor_dict):
        """
        Launch app in iconized mode
        :param app_descriptor_dict: example: {"testapp_id_for_later_killing": ["d:/testapp.bat"]}
        :return: N/A
        """
        #Send request to start a new app
        for key in app_descriptor_dict:
            self.launched_app_dict[key] = {
                "collector": self.launcher.create_console_wnd_for_app(app_descriptor_dict[key]),
                "params": app_descriptor_dict[key],
            }


def main():
    Iconizer().start_gui()


if __name__ == '__main__':
    main()