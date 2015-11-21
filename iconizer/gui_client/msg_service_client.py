from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory

__author__ = 'weijia'


class MsgServiceClient(object):
    def __init__(self):
        super(MsgServiceClient, self).__init__()
        factory = MsgServiceFactory()
        self.ufs_msg_service = factory.get_msg_service()
