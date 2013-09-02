import threading
from console.launcher import CrossGuiLauncher


class GuiLaunchServer(threading.Thread):
    def __init__(self, gui_factory):
        super(GuiLaunchServer, self).__init__()
        self.launcher = CrossGuiLauncher(gui_factory)

    def launch(self, app_descriptor_dict):
        self.launcher.send_launch_request(app_descriptor_dict)

    def run(self):
        self.launcher.start_cross_gui_launcher_no_return()