import os
import threading
import traceback

from Pyro4.errors import CommunicationError

from iconizer.iconizer_main import Iconizer
from iconizer.iconizer_client import IconizerClient
from ufs_tools.app_framework import AppConfig


# noinspection PyMethodMayBeStatic
class IconizerAppRoot(object):
    log_folder_name = "logs"

    def __init__(self, app_root_folder=None):
        super(IconizerAppRoot, self).__init__()
        self.front_end_task = self.get_frontend_task_descriptor()  # {"postgresql": ["scripts\\postgresql.bat"]}
        self.background_tasks = self.get_background_tasks()  # ({"web_server": ["manage.py", "runserver", "8110"]},)
        self.cleanup_tasks = self.get_cleanup_task_descriptors()
        self.app = AppConfig(app_root_folder)
        self.log_folder_full_path = self.app.get_or_create_app_data_folder(self.log_folder_name)
        self.iconizer = Iconizer(self.log_folder_full_path)
        self.client = IconizerClient()

    def start_iconized_applications(self):
        try:
            threading.Thread(target=self.start_task_starter).start()
            # self.iconizer.add_final_close_listener(self.final_cleanup)
            self.iconizer.add_close_listener(self.final_cleanup)
            self.iconizer.execute(self.front_end_task)

        except (KeyboardInterrupt, SystemExit):
            raise
            # print "stopping database"

    def get_cleanup_task_descriptors(self):
        """
        :return: # [{"stop_postgresql": ["scripts\\postgresql_stop.bat"]}]
        """
        return tuple()

    def start_task_starter(self):
        self.wait_for_pyro_server()
        self.sync_to_main_thread()
        self.start_background_tasks()

    def start_background_tasks(self):
        print "executing in remote!!!!!!"
        try:
            self.execute_tasks(self.background_tasks)
        except:
            traceback.print_exc()
            pass

    def wait_for_pyro_server(self):
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

    def execute_tasks(self, tasks):
        for task in tasks:
            self.client.execute_in_remote(task)

    def final_cleanup(self):
        self.execute_tasks(self.cleanup_tasks)

    def sync_to_main_thread(self):
        pass

    def get_frontend_task_descriptor(self):
        return {}

    def get_background_tasks(self):
        return []
