#!/usr/bin/env python
# -*- coding: utf-8 -*-
from iconizer.console.launcher import CrossGuiLauncher
from iconizer.qtconsole.PyQtGuiFactory import PyQtGuiFactory


class Iconizer(object):
    def start_gui(self):
        self.server = CrossGuiLauncher(PyQtGuiFactory())
        self.server.start()
        self.server.start_cross_gui_launcher_no_return()

    def execute(self, app_descriptor_dict):
        #Send request to start a new app
        self.server.launch(app_descriptor_dict)


def main():
    Iconizer().start_gui()

if __name__ == '__main__':
    main()