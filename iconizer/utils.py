from ufs_tools import find_callable_in_app_framework
from iconizer.iconizer_app_root_v2 import IconizerAppRootV2
from iconizer.iconizer_task_config import IconizerTaskConfig


# noinspection PyMethodMayBeStatic
class ScriptAppConfig(IconizerTaskConfig):

    def __init__(self, script_name):
        """
        Init a script app config instance
        :param script_name: the python script name. The script will be convert to .exe when freeze, so this config 
        instance will 
        """
        super(ScriptAppConfig, self).__init__()
        self.script_name = script_name

    def get_frontend_task_descriptor(self):
        executable = find_callable_in_app_framework(self.script_name)
        return {self.script_name: [executable]}


def start_script_app_iconized(script_app_name):
    script_app_config = ScriptAppConfig(script_app_name)
    IconizerAppRootV2(script_app_config).start_iconized_applications()
