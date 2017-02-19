# import traceback
import traceback
from console_output_collector import ConsoleOutputCollector
import os
from iconizer.logsys.logDir import logDir, ensure_dir
from msg_handler import GuiServiceMsgHandler
# import webbrowser
# import sys
# import time


def call_function_no_exception(func, *args):
    try:
        func(*args)
    except:
        traceback.print_exc()


def call_callbacks_in_list_no_exception(callback_list):
    for callback_func in callback_list:
        call_function_no_exception(callback_func)


class CrossGuiLauncher(object):
    """
    In this class, app id string is a string generated from app's path and param, and a number will be added
    to app id string if app path and param is identical for 2 running app. such as startBeanstalkd.bat and
    startBeanstalkd.bat-1.
    """

    def __init__(self, gui_factory, log_dir=None, python_executable=None):
        """
        * Create taskbar menu
        """
        super(CrossGuiLauncher, self).__init__()
        self.gui_factory = gui_factory
        self.taskbar_icon_app = self.gui_factory.create_taskbar_icon_app()
        self.app_list_ui_for_app_id_str_to_app_wnd_state = self.gui_factory.get_app_list()
        self.msg_handler = GuiServiceMsgHandler(self)
        self.app_id_str_to_console_wnd = {}
        self.wnd_to_console_dict = {}
        self.log_collector_to_menu_item_dict = {}
        self.wnd_to_app_id_str_dict = {}
        self.launched_app_dict = {}
        self.gui_factory.set_msg_callback(self.on_msg)
        # Called when user requesting closing app
        self.close_callback_list = []
        # Called when app notified all sub process before app will really quit
        self.final_close_callback_list = []
        self.log_dir = log_dir
        self.python_executable = python_executable

    #####################################
    # Callbacks
    #####################################
    def on_child_closed(self, child_wnd):
        """
        Called from GUI factory when the console child window is closed.
        :param child_wnd:
        :return:
        """
        self.app_list_ui_for_app_id_str_to_app_wnd_state[self.wnd_to_app_id_str_dict[child_wnd]] = \
            {"checked": False, "action": self.on_app_item_selected}

    def on_app_item_selected(self, app_id_str):
        # print 'selected: ', app_id
        minimized = self.app_id_str_to_console_wnd[app_id_str].toggle()
        self.app_list_ui_for_app_id_str_to_app_wnd_state[app_id_str] = {"checked": not minimized,
                                                                        "action": self.on_app_item_selected,
                                                                        "on_right_click": self.on_right_click
                                                                        }

    def on_right_click(self, app_title):
        console_wnd = self.app_id_str_to_console_wnd[app_title]
        console_output_manager = self.wnd_to_console_dict[console_wnd]
        if console_output_manager.is_app_ended():
            del self.app_id_str_to_console_wnd[app_title]
            del self.wnd_to_console_dict[console_wnd]
            del self.wnd_to_app_id_str_dict[console_wnd]
            for launched_app in self.launched_app_dict:
                if self.launched_app_dict[launched_app]["collector"] == console_output_manager:
                    del self.launched_app_dict[launched_app]
                    break
            del console_wnd
            del self.app_list_ui_for_app_id_str_to_app_wnd_state[app_title]
            del console_output_manager

    def on_quit_clicked(self):
        # self.window.hide()
        # self.icon.set_visible(False)
        # print 'on_quit_clicked, send KeyInterrupts to apps'
        call_callbacks_in_list_no_exception(self.close_callback_list)

        print 'wait for 10 seconds'
        # Use gui factory method, so UI will not be blocked
        self.gui_factory.timeout(5000, self.final_quit)

    #######################
    # External callable functions
    #######################
    def send_msg(self, msg):
        """
        Send message to GUI thread, so it will be handled in GUI thread
        :param msg:
        :return:
        """
        self.gui_factory.trigger(msg)

    def start_cross_gui_launcher_no_return(self):
        self.taskbar_icon_app["Show/Hide"] = self.app_list_ui_for_app_id_str_to_app_wnd_state.ui_widget.toggle
        self.taskbar_icon_app["Exit"] = self.on_quit_clicked
        self.gui_factory.start_msg_loop()
        print "launcher.py", "quitting msg loop"

    ###############################
    # Internal functions
    ###############################
    def final_quit(self):
        print 'start to killing apps'
        for log_collector in self.log_collector_to_menu_item_dict.keys():
            log_collector.kill_console_process_tree()

        print "before factory exit"
        self.gui_factory.abort_msg_loop()
        print "calling final close handlers"
        call_callbacks_in_list_no_exception(self.final_close_callback_list)

    def on_msg(self, data):
        self.msg_handler.handle_msg(data)

    #######################
    # App launch related
    #######################
    def execute_iconized(self, app_descriptor_dict):
        """
        Launch app in iconized mode
        :param app_descriptor_dict: example: {"test_app_id_for_later_killing": ["d:/test_app.bat", "param1", "param2"]}
        :return: N/A
        """
        # Send request to start a new app
        for key in app_descriptor_dict:
            if key in self.launched_app_dict:
                print "Application named: %s is already occupied" % key
                return
            print key, app_descriptor_dict[key]
            self.launched_app_dict[key] = {
                "collector": self.create_console_wnd_for_app(app_descriptor_dict[key]),
                "params": app_descriptor_dict[key],
                "app_id": key,
            }

    def create_console_wnd_for_app(self, param):
        """
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        """
        print "launching: ", param
        app_full_path = param[0]
        l = logDir(os.path.basename(app_full_path), self.log_dir)
        app_log_wnd = self.gui_factory.create_console_output_wnd(self, l.getLogFilePath())
        log_collector = ConsoleOutputCollector(l.getLogFilePath(), self.python_executable)
        cwd = os.getcwd()
        log_collector.run_app_in_window(app_log_wnd, cwd, param)
        self.wnd_to_console_dict[app_log_wnd] = log_collector
        app_log_wnd.set_title(app_full_path)

        cnt = 1
        app_name = os.path.basename(app_full_path)
        app_path = os.path.dirname(app_full_path)
        app_path_and_param_gen_str = "%s %s (%s)" % (app_name, str(param[1:]), app_path)
        if app_path_and_param_gen_str in self.app_id_str_to_console_wnd:
            while app_path_and_param_gen_str + '-' + str(cnt) in self.app_id_str_to_console_wnd:
                cnt += 1
            app_path_and_param_gen_str = app_path_and_param_gen_str + '-' + str(cnt)

        self.app_id_str_to_console_wnd[app_path_and_param_gen_str] = app_log_wnd
        self.wnd_to_app_id_str_dict[app_log_wnd] = app_path_and_param_gen_str
        self.log_collector_to_menu_item_dict[log_collector] = app_log_wnd

        self.app_list_ui_for_app_id_str_to_app_wnd_state[app_path_and_param_gen_str] = \
            {"checked": False,
             "action": self.on_app_item_selected,
             "on_right_click": self.on_right_click}
        return log_collector


def main():
    from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend

    CrossGuiLauncher(PyQtGuiBackend()).start_cross_gui_launcher_no_return()


if __name__ == '__main__':
    main()
