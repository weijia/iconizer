from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from iconizer.pyro_service_obj import PyroServiceObj
from iconizer.console.launcher import CrossGuiLauncher, call_function_no_exception, call_callbacks_in_list_no_exception
from iconizer.qtconsole.pyqt_ui_backend import PyQtGuiBackend


class IconizerServer(PyroServiceObj):
    def __init__(self, log_dir=None, python_executable=None):
        super(IconizerServer, self).__init__(ICONIZER_SERVICE_NAME)
        #self.launched_app_dict = {}
        self.launch_server = None
        #Create windows
        self.gui_launch_manger = None
        self.log_dir = log_dir
        self.uri = None
        self.python_executable = python_executable

    #########################
    # Called through pyro only
    #########################
    def send_msg(self, msg):
        """
        Send command msg to GUI
        """
        print "sending msg:", msg
        self.get_gui_launch_manager().send_msg(msg)

    #noinspection PyMethodMayBeStatic
    def is_running(self):
        print "is_running_called"
        return True

    ######################
    # Internal functions
    ######################
    def start_gui_no_return(self, app_descriptor_dict={}):
        #Add closing callback, so when GUI was closing, Iconizer will got notified
        self.add_final_close_listener(self.on_final_close)

        #Start background thread running pyro service
        self.start()

        #Execute app must be called in the main thread
        call_function_no_exception(self.get_gui_launch_manager().execute_inconized, app_descriptor_dict)
        self.get_gui_launch_manager().start_cross_gui_launcher_no_return()

    def on_final_close(self):
        self.pyro_shutdown()

    def get_gui_launch_manager(self):
        if self.gui_launch_manger is None:
            self.gui_launch_manger = CrossGuiLauncher(PyQtGuiBackend(), self.log_dir, self.python_executable)
        return self.gui_launch_manger

    def add_final_close_listener(self, final_close_callback):
        self.get_gui_launch_manager().final_close_callback_list.append(final_close_callback)

    def add_close_listener(self, close_callback):
        self.get_gui_launch_manager().close_callback_list.append(close_callback)