#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_iconizer
----------------------------------

Tests for `iconizer` module.
"""
import logging
from threading import Thread
from time import sleep

import unittest

from iconizer import Iconizer
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory


class BackgroundTask(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(BackgroundTask, self).__init__(group, target, name, args, kwargs, verbose)

    def run(self):
        sleep(10)
        s = MsgServiceFactory().get_msg_service()
        receiving_ch = "receiver_channel"
        c = s.create_channel(receiving_ch)
        s.send_to(ICONIZER_SERVICE_NAME,  {"command": "register_to_clipboard",
                                           "target": c.get_channel_full_name()})
        while True:
            m = c.get_msg()
            # print m
            self.on_clip(m)

    def on_clip(self, msg):
        print msg


class TestIconizer(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        logging.basicConfig(level=logging.DEBUG)
        BackgroundTask().start()
        Iconizer().execute({"test_app_id_for_later_killing": ["dir"]})

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()