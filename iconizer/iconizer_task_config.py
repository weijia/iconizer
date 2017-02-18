import os

from ufs_tools.app_framework import AppConfig


# noinspection PyMethodMayBeStatic
from ufs_tools.app_tools import get_executable

from iconizer.django_in_iconizer.django_server import DjangoServer, DjangoServerExe


def is_binary_executable(app_executable_full_path):
    return "python.exe" in app_executable_full_path or ".py" in app_executable_full_path


class IconizerTaskConfig(object):
    def __init__(self):
        super(IconizerTaskConfig, self).__init__()
        app_executable_full_path = get_executable()
        if is_binary_executable(app_executable_full_path):
            self.django_server = DjangoServer()
        else:
            self.django_server = DjangoServerExe()
        # root_folder = os.path.basename(get_folder(get_inspection_frame(2)))
        root_folder = os.path.dirname(app_executable_full_path)
        # print "root folder name:", root_folder
        self.app = AppConfig(root_folder)

    def get_frontend_task_descriptor(self):
        return {}

    def get_background_tasks(self):
        return []

    def get_cleanup_task_descriptors(self):
        """
        :return: # [{"stop_postgresql": ["scripts\\postgresql_stop.bat"]}]
        """
        return tuple()

    def get_app_config(self):
        return self.app
