import os

from ufs_tools import get_folder
from ufs_tools.inspect_utils import get_inspection_frame

from iconizer.django_in_iconizer.django_server import DjangoServer
from iconizer.iconizer_app_root import IconizerAppRoot


class DjangoStarter(IconizerAppRoot):
    django_main_script_name = "manage.py"
    app_root_folder_name = "server_for_django_15_and_below"

    def __init__(self):
        self.django_server = DjangoServer(self.django_main_script_name)
        root_folder_name = os.path.basename(get_folder(get_inspection_frame(2)))
        print "root folder name:", root_folder_name
        super(DjangoStarter, self).__init__(root_folder_name)

    def init_ufs_db(self):
        self.django_server.execute_cmd("migrate")
        self.django_server.execute_cmd("create_default_super_user")
