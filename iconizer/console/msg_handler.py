import json
import Pyro4
import beanstalkc


class GuiServiceMsgHandler(object):
    def __init__(self, gui_launch_manger):
        super(GuiServiceMsgHandler, self).__init__()
        self.gui_launch_manger = gui_launch_manger
        self.gui_factory = gui_launch_manger.gui_factory
        self.wnd2target = {}
        self.target2wnd = {}
        self.handle2browser = {}

    def handle_msg(self, msg):
        if msg["command"] == "launch":
            print "apps: ", msg["apps"]
            self.gui_launch_manger.execute_inconized(msg["apps"])
        elif msg["command"] == "DropWnd":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        elif msg["command"] == "DestroyDropWnd":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            #del self.target2wnd[msg]
            wnd.deleteLater()
        elif msg["command"] == "Browser":
            url = msg["url"]
            handle = msg["handle"]
            self.gui_factory.show_browser(handle, url)
        elif msg["command"] == "DestroyBrowser":
            handle = msg["handle"]
            self.gui_factory.remove_browser(handle)
        elif msg["command"] == "notify":
            msg_str = msg["msg"]
            self.gui_factory.msg(msg_str)

    def drop_callback(self, drop_wnd, urls):
        #print "dropped: ", urls
        #print drop_wnd, self.wnd2target
        target = self.wnd2target[drop_wnd]
        #target_queue = beanstalkServiceBase(target)
        if not (self.gui_launch_manger.msg_service is None):
            try:
                self.gui_launch_manger.msg_service.sendto(target, {"command": "dropped", "urls": urls})
            except:
                import traceback
                traceback.print_exc()
        #try:
        #    name_server = Pyro4.locateNS()
        #    proxy_uri = name_server.lookup(target)
        #    proxy = Pyro4.Proxy(proxy_uri)
        #    proxy.send_msg({"command": "dropped", "urls": urls})
        #except:
        #    import traceback
        #    traceback.print_exc()
        ############################
        #beanstalk_server_host = '127.0.0.1'
        #beanstalk_server_port = 8212
        #beanstalk = beanstalkc.Connection(host=beanstalk_server_host, port=beanstalk_server_port)
        #beanstalk.put(json.dumps({"command": "dropped", "urls": urls}))