#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Pyro4
from Pyro4.errors import CommunicationError
from iconizer.iconizer_client import IconizerClient
from iconizer.iconizer_server import IconizerServer
from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend

Pyro4.config.COMMTIMEOUT=0.5


log = logging.getLogger(__name__)


class Iconizer(IconizerServer):
    ######################
    # External interface
    ######################
    def execute(self, app_descriptor_dict):
        if not self.is_server_already_started():
            self.start_gui_no_return(app_descriptor_dict)
        else:
            self.iconizer_client.execute_in_remote(app_descriptor_dict)

    def __init__(self, log_dir=None, python_executable=None):
        super(Iconizer, self).__init__(log_dir, python_executable)
        self.iconizer_client = IconizerClient()

    def is_server_already_started(self):
        try:
            self.iconizer_client.is_running()
            log.debug("is_server_already_started: Is running is True")
            return True
        except CommunicationError:
            log.error("is_server_already_started: Server not running")
            import traceback
            traceback.print_exc()
            return False

    def register(self):
        self.iconizer_client.register_to_name_server()


def main():
    Iconizer().execute({"test_app_id_for_later_killing": ["dir"]})


if __name__ == '__main__':
    main()