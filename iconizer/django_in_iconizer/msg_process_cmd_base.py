import logging
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management import BaseCommand
import sys

from tendo.singleton import SingleInstance

from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase
from ufs_tools.inspect_utils import get_inspection_frame

from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory
import traceback

__author__ = 'weijia'


class MsgProcessCommandBase(DjangoCmdBase):

    def __init__(self):
        super(MsgProcessCommandBase, self).__init__()
        factory = MsgServiceFactory()
        self.ufs_msg_service = factory.get_msg_service()
        self.channel = None
        caller_file = get_inspection_frame(2)
        app_signature = caller_file.replace("/", "_").replace("\\", "_").replace(":", "_")
        # Keep the instance, the lock file will be deleted whenever the instance is deleted
        self.me = SingleInstance(app_signature)
        username = self.get_username()
        print "username is:", username
        self.admin_user = User.objects.get(username=username)

    def msg_loop(self):
        channel = self.register_to_service()
        while True:
            msg = channel.get_msg()
            if self.ufs_msg_service.is_exit(msg):
                break
            try:
                self.process_msg(msg)
            except Exception, e:
                traceback.print_exc()
                pass
        print "exiting handle function"

    # noinspection PyMethodMayBeStatic
    def register_to_service(self):
        return None

    def get_channel(self, channel_name=None):
        if self.channel is None:
            if channel_name is None:
                raise "Please provide a channel name for init"
            self.channel = self.ufs_msg_service.create_channel(channel_name)
        return self.channel
