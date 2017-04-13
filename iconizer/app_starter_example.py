import logging
from ufs_tools.python_app_utils.base import AppBase

from iconizer.utils import start_script_app_iconized

AppBase().add_default_module_path()


__author__ = 'weijia'

log = logging.getLogger(__name__)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    start_script_app_iconized("universal_controller_app")
