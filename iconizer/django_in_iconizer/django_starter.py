import os

from ufs_tools import get_folder
from ufs_tools.app_tools import get_executable
from ufs_tools.inspect_utils import get_inspection_frame

from iconizer.django_in_iconizer.django_server import DjangoServer, DjangoServerExe
from iconizer.iconizer_app_root import IconizerAppRoot


class DjangoStarter(IconizerAppRoot):

    def __init__(self):
        app_executable_full_path = get_executable()
        if "python.exe" in app_executable_full_path or ".py" in app_executable_full_path:
            self.django_server = DjangoServer()
        else:
            self.django_server = DjangoServerExe()
        # root_folder = os.path.basename(get_folder(get_inspection_frame(2)))
        root_folder = os.path.dirname(app_executable_full_path)
        print "root folder name:", root_folder
        super(DjangoStarter, self).__init__(root_folder)

    def init_ufs_db(self):
        # self.django_server.execute_cmd("migrate auth")
        # self.django_server.execute_cmd("migrate sites")
        self.django_server.execute_cmd("migrate")
        self.django_server.execute_cmd("create_default_super_user")
