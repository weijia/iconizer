import os


class DjangoServer(object):
    default_django_manage_script = "manage.py"

    def __init__(self, django_manage_script=None):
        super(DjangoServer, self).__init__()
        if django_manage_script is None:
            self.django_manage_script = self.default_django_manage_script
        else:
            self.django_manage_script = django_manage_script

    def get_task_descriptor(self, task_name, param_list=[]):
        task_name_and_param = [self.django_manage_script, task_name]
        task_name_and_param.extend(param_list)
        return {task_name: task_name_and_param}

    # noinspection PyMethodMayBeStatic
    def get_cmd_str(self, cmd_name, param_list=[]):
        return "python %s %s" % (self.django_manage_script, cmd_name)

    def execute_cmd(self, django_cmd):
        os.system(self.get_cmd_str(django_cmd))
