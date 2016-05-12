from iconizer.django_in_iconizer.django_server import DjangoServer
from iconizer.django_in_iconizer.postgresql_checker import PostgreSqlChecker
from iconizer.iconizer_app_root import IconizerAppRoot


class DjangoStarter(IconizerAppRoot):
    django_main_script_name = "manage.py"
    app_root_folder_name = "server_for_django_15_and_below"

    def __init__(self):
        self.django_server = DjangoServer(self.django_main_script_name)
        super(DjangoStarter, self).__init__()

    def init_ufs_db(self):
        self.django_server.execute_cmd("migrate")
        self.django_server.execute_cmd("create_default_super_user")
