class GuiFactoryBase(object):
    def __init__(self):
        pass

    def create_taskbar_icon_app(self):
        pass

    def create_console_output_wnd(self, parent, log_file_path=None):
        pass

    def start_msg_loop(self):
        pass

    def timeout(self):
        pass

    def get_app_list(self):
        pass

    def create_drop_target(self, callback):
        pass

    def remove_browser(self, handle):
        pass

    def show_browser(self, handle, url):
        pass

    def msg(self, msg):
        pass

    def register_to_clipboard_event(self, handle):
        pass

    def get_clipboard_data(self):
        pass
