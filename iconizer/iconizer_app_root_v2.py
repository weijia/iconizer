import os
import threading
import traceback

from Pyro4.errors import CommunicationError

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient


# noinspection PyMethodMayBeStatic
class IconizerAppRootV2(object):
    log_folder_name = "logs"

    def __init__(self, iconizer_config):
        super(IconizerAppRootV2, self).__init__()
        self.iconizer_config = iconizer_config
        self.app = iconizer_config.get_app_config()
        self.log_folder_full_path = self.app.get_or_create_app_data_folder(self.log_folder_name)
        self.iconizer = Iconizer(self.log_folder_full_path)
        self.client = IconizerClient()

    def start_iconized_applications(self):
        try:
            threading.Thread(target=self.start_task_starter).start()
            # self.iconizer.add_final_close_listener(self.final_cleanup)
            self.iconizer.add_close_listener(self.final_cleanup)
            self.iconizer.execute(self.iconizer_config.get_frontend_task_descriptor())

        except (KeyboardInterrupt, SystemExit):
            raise
            # print "stopping database"

    def start_task_starter(self):
        self.wait_for_pyro_server()
        self.iconizer_config.sync_to_main_thread()
        self.start_background_tasks()

    def start_background_tasks(self):
        print "executing in remote!!!!!!"
        try:
            self.execute_tasks(self.iconizer_config.get_background_tasks())
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
        self.execute_tasks(self.iconizer_config.get_cleanup_task_descriptors())

    def sync_to_main_thread(self):
        pass
