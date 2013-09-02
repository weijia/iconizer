#!/usr/bin/env python
# -*- coding: utf-8 -*-
from guiserver import GuiLaunchServer
from qtconsole.PyQtGuiFactory import PyQtGuiFactory

class Iconizer(object):
    def __init__(self):
        self.server = GuiLaunchServer(PyQtGuiFactory)
        self.server.start()

    def execute(self, app_descriptor_dict):
        #Send request to start a new app
        self.server.launch(app_descriptor_dict)


def main():
    Iconizer()

if __name__ == '__main__':
    main()