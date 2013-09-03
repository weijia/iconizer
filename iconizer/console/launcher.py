#import traceback
import threading
import Pyro4
from console_output_collector import ConsoleOutputCollector
import os
from iconizer.logsys.logDir import logDir, ensure_dir
from msg_handler import GuiServiceMsgHandler
#import webbrowser
#import sys
#import time


class CrossGuiLauncher(object):
    def __init__(self, gui_factory):
        """
        * Create taskbar menu
        """
        super(CrossGuiLauncher, self).__init__()
        self.gui_factory = gui_factory
        self.taskbar_icon_app = self.gui_factory.create_taskbar_icon_app()
        self.app_list_ui = self.gui_factory.get_app_list()
        self.taskbar_icon_app["Show/Hide"] = self.app_list_ui.app_list.toggle
        self.taskbar_icon_app["Exit"] = self.on_quit_clicked

        super(CrossGuiLauncher, self).__init__()
        self.app_name_to_task_dict = {}
        #self.basic_app_name_to_task_dict = {}
        self.wnd_to_console_dict = {}
        self.task_to_menu_item_dict = {}
        self.wnd2str = {}
        self.msg_handler = GuiServiceMsgHandler(gui_factory)
        #self.must_shutdown = False

    def start_msg_loop(self):
        self.gui_factory.start_msg_loop()

    def on_app_item_selected(self, app_id):
        #print 'selected: ', app_id
        minimized = self.on_menu_clicked(app_id)
        self.app_list_ui[app_id] = {"checked": not minimized, "action": self.on_app_item_selected}

    #####################################
    # Event handlers
    #####################################
    def on_menu_clicked(self, menu_text):
        return self.app_name_to_task_dict[menu_text].toggle()

    def on_child_closed(self, child_wnd):
        self.app_list_ui[self.wnd2str[child_wnd]] = {"checked": False, "action": self.on_app_item_selected}

    def on_quit_clicked(self):
        #self.window.hide()
        #self.icon.set_visible(False)
        print 'on_quit_clicked'
        #self.msg_service.stop_all_msg_service_clients(self.session_id)

        print 'wait for 10 seconds'
        #Use gui factory method, so UI will not be blocked
        self.gui_factory.timeout(5000, self.final_quit)

    ###############################
    # Internal functions
    ###############################
    def final_quit(self):
        print 'start to killing apps'
        #kill all app except msg service
        for log_collector in self.task_to_menu_item_dict.keys():
            log_collector.kill_console_process_tree()

        #Kill msg service
        #if not (self.msg_service_app is None):
        #    self.msg_service_app.kill_console_process_tree()

        print "before factory exit"
        print 'all application killed, after main_quit'
        self.gui_factory.exit()
        print "setting shutdown flag"
        self.close_callback()
        #sys.exit(0)

    #######################
    # App launch related
    #######################

    def handle_msg(self, data):
        self.msg_handler.handle_msg(data)

    def create_console_wnd_for_app(self, param):
        """
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        """
        cwd = os.getcwd()
        log_root = os.path.join(cwd, "logs")
        ensure_dir(log_root)
        l = logDir(os.path.basename(param[0]), log_root)
        child_wnd = self.gui_factory.create_console_output_wnd(self, l.getLogFilePath())
        collector = ConsoleOutputCollector()
        cwd = os.getcwd()
        collector.runConsoleApp(child_wnd, cwd, param)
        self.wnd_to_console_dict[child_wnd] = collector
        child_wnd.set_title(param[0])

        cnt = 1
        app_name = os.path.basename(param[0])
        app_path = os.path.dirname(param[0])
        app_path_and_param_gen_str = "%s(%s) params: %s" % (app_name, app_path, str(param[1:]))
        if self.app_name_to_task_dict.has_key(app_path_and_param_gen_str):
            while self.app_name_to_task_dict.has_key(app_path_and_param_gen_str + '-' + str(cnt)):
                cnt += 1
            app_path_and_param_gen_str = app_path_and_param_gen_str + '-' + str(cnt)

        self.app_name_to_task_dict[app_path_and_param_gen_str] = child_wnd
        self.wnd2str[child_wnd] = app_path_and_param_gen_str
        #self.app_name_to_collector[app_path_and_param_gen_str] = collector
        self.task_to_menu_item_dict[collector] = child_wnd
        #self.taskbar_icon_app[app_path_and_param_gen_str] = self.on_app_item_selected
        self.app_list_ui[app_path_and_param_gen_str] = {"checked": False, "action": self.on_app_item_selected}
        return collector

    #######################
    # External callable
    #######################
    def add_close_listener(self, callback):
        self.close_callback = callback

    def start_cross_gui_launcher_no_return(self, app_descriptor_dict={}):
        self.start_msg_loop()


def main():
    from qtconsole.PyQtGuiFactory import PyQtGuiFactory
    CrossGuiLauncher(PyQtGuiFactory).start_cross_gui_launcher_no_return()


if __name__ == '__main__':
    main()