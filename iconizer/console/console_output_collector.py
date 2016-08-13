import threading
import subprocess
import os

from iconizer.iconizer_utils.str_utils import decode_str
from iconizer.win import sysprocess
import iconizer.logsys.logDir as logDir
from iconizer.logsys.logSys import *
import traceback

CREATE_NO_WINDOW = 0x8000000


class ConsoleCollectWorkerThread(threading.Thread):
    def __init__(self, target, file_descriptor, app_name='unknown', output_to_console=False, logFilePath=None):
        self.target = target
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.file_descriptor = file_descriptor
        self.app_name = app_name
        self.output_to_console = output_to_console
        self.logFilePath = logFilePath

    def open_log_if_needed(self):
        if not (self.logFilePath is None):
            try:
                f = open(self.logFilePath, "w")
            except:
                cl("Can not open: %s" % self.logFilePath)
                f = None
        else:
            f = None
        return f

    def run(self):
        # print 'running'
        f = self.open_log_if_needed()
        while not self.quitFlag:
            # print 'before readline'
            read_data = self.file_descriptor.readline()
            read_data = decode_str(read_data)
            if read_data == '':
                # print 'read_data is empty'
                self.quit()
            if read_data is None:
                self.quit()
                # print 'quit'
                break
            if self.output_to_console:
                # print 'got output:', self.appname, ':  ',read_data
                info(read_data)
                pass
            if not (f is None):
                try:
                    f.write(read_data)
                except:
                    pass
            self.target.update_view_callback(read_data)
        if not (f is None):
            f.close()
        print 'quitting run: ', self.app_name

    def quit(self):
        self.quitFlag = True


class ConsoleOutputCollector(object):
    """
    Create a console window and start a process. Collect the logs generated by the process.
    """

    normal_priority_tasks = ["webserver-cgi",
                             "startBeanstalkd.bat",
                             "mongodb.bat",
                             "cherrypyServerV4",
                             "monitorServiceV2"
                             ]

    def __init__(self, log_root_path=None, python_executable=None):
        self.log_collector_thread_list = []
        self.process_list = []
        self.stopped = False
        self.log_root_path = log_root_path
        self.python_executable = python_executable
        self.cwd = None
        # self.app_path_and_param = None
        self.real_execute_path_and_param_list = None
        self.app_full_path = None
        self.console_window = None

    def get_python_executable(self):
        if self.python_executable is None:
            possible_python_exe_path = []
            # print os.environ
            try:
                possible_python_exe_path.append(sys.executable)
                possible_python_exe_path.append(os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts/pythonw.exe'))
                # print 'using virtual env:', pythonWinPathList[0], progAndParam
            except:
                pass
            possible_python_exe_path.extend(
                ['c:/Python27/pythonw.exe', 'd:/python27/pythonw.exe', 'd:/python25/pythonw.exe',
                 'c:/python27/pythonw.exe', 'c:/python26/pythonw.exe', 'c:/python25/pythonw.exe'])
            for i in possible_python_exe_path:
                if os.path.exists(i):
                    target_python_executable = i
                    break
                else:
                    # print i, ", does not exist"
                    pass
        else:
            target_python_executable = self.python_executable
        return target_python_executable

    def run_app_in_window(self, target, cwd, app_or_script_path_and_param_list):
        if not self.is_app_or_script_exists(app_or_script_path_and_param_list):
            print "%s does not exist" % self.app_full_path
            return
        self.validate_cur_working_dir(cwd)
        self.console_window = target

        self.set_window_title(app_or_script_path_and_param_list)

        self.get_actual_execute_path_and_param_list(app_or_script_path_and_param_list)
        print self.real_execute_path_and_param_list

        if True:  # try:
            self.start_app_and_collect_logs(app_or_script_path_and_param_list, target)
            # print 'launch ok'
        else:  # except:
            print 'launch exception'
            # self.appStarted = True

    def is_app_or_script_exists(self, app_or_script_path_and_param_list):
        self.app_full_path = app_or_script_path_and_param_list
        if type(self.app_full_path) == list:
            possible_installed_python_script = os.path.join(os.path.dirname(self.get_python_executable()),
                                                            self.app_full_path[0])
            if os.path.exists(possible_installed_python_script):
                self.app_full_path = possible_installed_python_script
                return True
            self.app_full_path = os.path.abspath(self.app_full_path[0])
            if os.path.exists(self.app_full_path):
                return True
        return False

    def set_window_title(self, app_or_script_path_and_param_list):
        try:
            self.console_window.set_title(str(app_or_script_path_and_param_list))
        except:
            traceback.print_exc()
            print "set title not supported"
            # print target

    def start_app_and_collect_logs(self, app_or_script_path_and_param_list, console_window):
        # print self.real_execute_path_and_param_list
        # self.validate_executable_path()  # the path is already checked in run_app_in_window
        p = subprocess.Popen(self.real_execute_path_and_param_list, cwd=self.cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, bufsize=0,
                             creationflags=CREATE_NO_WINDOW)
        self.process_list.append(p)
        # print "created pid:", p.pid
        self.update_process_priority(app_or_script_path_and_param_list, p)
        log_path_base_name = os.path.basename(
            app_or_script_path_and_param_list[0])  # + str(app_or_script_path_and_param_list[1:])
        normal_log_path = logDir.logDir(log_path_base_name + "_normal", self.log_root_path)
        err_log_path = logDir.logDir(log_path_base_name + "_error", self.log_root_path)
        thr1 = ConsoleCollectWorkerThread(console_window, p.stdout, app_or_script_path_and_param_list[0],
                                          False, normal_log_path.getLogFilePath())
        thr1.start()
        self.log_collector_thread_list.append(thr1)
        thr2 = ConsoleCollectWorkerThread(console_window, p.stderr, app_or_script_path_and_param_list[0],
                                          True, err_log_path.getLogFilePath())
        thr2.start()
        self.log_collector_thread_list.append(thr2)

    def update_process_priority(self, app_or_script_path_and_param_list, p):
        find_flag = False
        for z in self.normal_priority_tasks:
            if app_or_script_path_and_param_list[0].find(z) != -1:
                # Need normal priority for this app
                find_flag = True
        if not find_flag:
            sysprocess.set_priority(p.pid, 1)
            pass
            # print "setting pid: %d, %s to below normal priority"%(p.pid, app_or_script_path_and_param_list[0])
        else:
            # print "pid: %d, %s use normal priority"%(p.pid, app_or_script_path_and_param_list[0])
            pass
            # print 'taskid:%d, pid:%d'%(int(p._handle), int(p.pid))

    # def validate_executable_path(self):
    #     if not os.path.exists(self.real_execute_path_and_param_list[0]):
    #         print "path does not exist: ", self.real_execute_path_and_param_list[0]

    def validate_cur_working_dir(self, cwd):
        self.cwd = cwd
        if not (os.path.exists(self.cwd)):
            print 'execution path does not exist: ', self.cwd
        # self.app_path_and_param = app_or_script_path_and_param_list

    def get_actual_execute_path_and_param_list(self, app_or_script_path_and_param_list):
        ext = os.path.splitext(self.app_full_path)[1]
        # print 'ext is:', ext
        if ".py" == ext:
            target_python_executable = self.get_python_executable()
            self.real_execute_path_and_param_list = [target_python_executable, '-u']
            self.real_execute_path_and_param_list.extend(app_or_script_path_and_param_list)  # Param 2 is the app
        else:
            self.real_execute_path_and_param_list = []
            self.real_execute_path_and_param_list.extend(app_or_script_path_and_param_list)

    def kill_console_process_tree(self):
        # TODO: do we need to kill applications?
        for i in self.process_list:
            print 'processing:', i.pid, ", handle: ", int(i._handle)
            sysprocess.killChildProcessTree(i.pid)
            sysprocess.TerminateProcess(i)
        for i in self.log_collector_thread_list:
            i.quit()

    def send_stop_signal(self):
        pass
