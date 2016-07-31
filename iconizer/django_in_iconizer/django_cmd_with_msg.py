import traceback

from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory


class DjangoCmdWithMsg(DjangoCmdBase):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(DjangoCmdWithMsg, self).__init__(stdout, stderr, no_color)
        factory = MsgServiceFactory()
        self.ufs_msg_service = factory.get_msg_service()
        self.channel = None

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

    def register_to_service(self):
        pass

    def get_channel(self, channel_name=None):
        if self.channel is None:
            if channel_name is None:
                raise "Please provide a channel name for init"
            self.channel = self.ufs_msg_service.create_channel(channel_name)
        return self.channel