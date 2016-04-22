import os
import threading
import traceback

from Pyro4.errors import CommunicationError

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient
from libtool.app_framework import AppConfig


class IconizerAppRoot(object):
    front_end_task = dict()  # {"postgre_sql": ["scripts\\postgresql.bat"]}
    background_tasks = tuple()  # ({"web_server": ["manage.py", "runserver", "8110"]},)
    app_root_folder_name = "."
    log_folder = "logs"
    cleanup_tasks = tuple()  # [{"stop_postgre_sql": ["scripts\\postgresql_stop.bat"]}]

    def __init__(self):
        super(IconizerAppRoot, self).__init__()
        self.app = AppConfig(os.path.realpath(__file__), self.app_root_folder_name)
        self.log_folder = self.app.get_or_create_app_data_folder(self.log_folder)
        self.iconizer = Iconizer(self.log_folder)
        self.client = IconizerClient()

    def start_iconized_applications(self):
        try:
            threading.Thread(target=self.start_task_starter).start()
            # i.start_name_server()
            # i.add_close_listener(stop_services_and_web_servers)
            # i.add_final_close_listener(stop_postgresql)
            # i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main

            # i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})
            self.iconizer.add_final_close_listener(self.final_cleanup)
            self.iconizer.execute(self.front_end_task)

        except (KeyboardInterrupt, SystemExit):
            raise
            # print "stopping database"

    def start_task_starter(self):
        cnt = 100
        while True:
            if cnt < 0:
                raise "No server found"
            try:
                if self.client.is_running():
                    break
            except CommunicationError:
                continue
            cnt -= 1
        self.sync_to_main_thread()
        print "executing in remote!!!!!!"
        try:
            self.execute_tasks(self.background_tasks)
        except:
            traceback.print_exc()
            pass

    def execute_tasks(self, tasks):
        for task in tasks:
            self.client.execute_in_remote(task)

    def final_cleanup(self):
        self.execute_tasks(self.cleanup_tasks)

    def sync_to_main_thread(self):
        pass
