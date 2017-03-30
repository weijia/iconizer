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
        # root_folder = os.path.basename(get_folder(get_inspection_frame(2)))
        self.executable = get_executable()
        root_folder = os.path.dirname(self.executable)
        # print "root folder name:", root_folder
        self.app = AppConfig(root_folder)

    def get_frontend_task_descriptor(self):
        return {"dummy task name": ["dummy task executable", "dummy param1"]}

    # noinspection PyMethodMayBeStatic
    def get_background_tasks(self):
        return []

    def start_other_tasks_depends_on_frontend_task(self):
        pass

    def get_cleanup_task_descriptors(self):
        """
        :return: # [{"stop_postgresql": ["scripts\\postgresql_stop.bat"]}]
        """
        return tuple()

    def get_app_config(self):
        return self.app


class IconizerDjangoTaskConfig(IconizerTaskConfig):
    def __init__(self):
        super(IconizerDjangoTaskConfig, self).__init__()
        if is_binary_executable(self.executable):
            self.django_server = DjangoServer()
        else:
            self.django_server = DjangoServerExe()
