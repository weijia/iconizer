class DjangoInIconizer(object):
    django_manage_script = "manage_with_conf.py"

    def get_django_task(self, task_name, param_list=[]):
        task_name_and_param = [self.django_manage_script, task_name]
        task_name_and_param.extend(param_list)
        return {task_name: task_name_and_param}
