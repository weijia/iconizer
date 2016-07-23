import os

from ufs_tools.app_framework import get_executable_folder


class DjangoServerBase(object):
    """
    Full path must be provided, so the executed app can have the correct folder info
    """
    def __init__(self, django_manage_script=None):
        super(DjangoServerBase, self).__init__()
        if django_manage_script is None:
            self.django_manage_script = self.default_django_manage_script
        else:
            self.django_manage_script = django_manage_script
        self.django_manage_script = os.environ.get("MANAGE_PY", self.django_manage_script)
        self.exe_folder = get_executable_folder()

    def get_full_path(self, filename):
        return os.path.join(self.exe_folder, filename)

    def get_task_descriptor(self, task_name, param_list=None):
        param_list = param_list or []
        task_name_and_param = [self.get_full_path(self.django_manage_script), task_name]
        task_name_and_param.extend(param_list)
        return {task_name: task_name_and_param}

    def execute_cmd(self, django_cmd):
        print "!!!!!!!!!!!!!!! cur folder:", os.getcwd()
        try:
            cmd_str = self.get_cmd_str(django_cmd)
            print cmd_str
            os.system(cmd_str)
        except:
            import traceback
            traceback.print_exc()


class DjangoServer(DjangoServerBase):
    default_django_manage_script = "manage.py"

    # noinspection PyMethodMayBeStatic
    def get_cmd_str(self, cmd_name, param_list=[]):
        return "python %s %s" % (self.django_manage_script, cmd_name)

    def get_run_server_task_descriptor(self, params=None):
        return self.get_task_descriptor("runserver", ["0.0.0.0:8110"])


class DjangoServerExe(DjangoServerBase):
    default_django_manage_script = "manage.exe"

    # noinspection PyMethodMayBeStatic
    def get_cmd_str(self, cmd_name, param_list=[]):
        exe_folder = get_executable_folder()
        print "exe_folder in django_server:", exe_folder
        return "%s %s" % (self.get_full_path(self.django_manage_script), cmd_name)

    # noinspection PyMethodMayBeStatic
    def get_run_server_task_descriptor(self, params=None):
        params = params or []
        exe_folder = get_executable_folder()
        cmd_and_param = [self.get_full_path("cherrypy_server.exe")]
        cmd_and_param.extend(params)
        # print "pwd:", os.getcwd()
        # print "!!!!!!!!!!!!!!!!!!!!!!!!!", exe_folder
        # os.chdir(exe_folder)
        return {"run server": cmd_and_param}
