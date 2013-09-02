import threading
import subprocess
import os
from iconizer.win import sysprocess

CREATE_NO_WINDOW = 0x8000000
#import beanstalkc
import iconizer.logsys.logDir as logDir
from iconizer.logsys.logSys import *
try:
    import pywintypes
except:
    pass
import traceback


class taskConsoleThread(threading.Thread):
    def __init__(self, target, fileD, appname='unknown', output_to_console=False, logFilePath=None):
        self.target = target
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.fileD = fileD
        self.appname = appname
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
        #print 'running'
        f = self.open_log_if_needed()
        while not self.quitFlag:
            #print 'before readline'
            err = self.fileD.readline()
            try:
                err = err.decode("gbk")
            except:
                try:
                    err = err.decode("utf8")
                except:
                    pass
                #print 'after readline'
            if err == '':
                #print 'err is empty'
                self.quit()
            if err is None:
                self.quit()
                #print 'quit'
                break
            if self.output_to_console:
                #print 'got output:', self.appname, ':  ',err
                info(err)
                pass
            if not (f is None):
                try:
                    f.write(err)
                except:
                    pass
            self.target.updateViewCallback(err)
        if not (f is None):
            f.close()
        print 'quitting run: ', self.appname

    def quit(self):
        self.quitFlag = True


def execute_app(app_full_path, param_list=[], cur_working_dir=None):
    ext = os.path.splitext(app_full_path)[1]
    if cur_working_dir is None:
        cur_working_dir = libsys.get_root_dir()
    pythonWinPathList = []
    try:
        pythonWinPathList.append(os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts/pythonw.exe'))
        #print 'using virtual env:', pythonWinPathList[0], progAndParam
    except:
        pass
    if ".py" == ext:
        pythonWinPathList.extend(['c:/Python27/pythonw.exe', 'd:/python27/pythonw.exe', 'd:/python25/pythonw.exe',
                                  'c:/python27/pythonw.exe', 'c:/python26/pythonw.exe', 'c:/python25/pythonw.exe'])
        for i in pythonWinPathList:
            if os.path.exists(i):
                targetPythonExePath = i
                break
            else:
                print i, ", does not exist"
                pass
        app_path_and_param_list = [targetPythonExePath, '-u']
        app_path_and_param_list.append(app_full_path)#Param 2 is the app
    else:
        app_path_and_param_list = []
        app_path_and_param_list.append(app_full_path)

    app_path_and_param_list.extend(param_list)

    if True:#try:
        if not os.path.exists(app_path_and_param_list[0]):
            print "path does not exist: ", app_path_and_param_list[0]
            #print subprocess.PIPE
        p = subprocess.Popen(app_path_and_param_list, cwd=cur_working_dir, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0, creationflags=CREATE_NO_WINDOW)
        return p
        #print "created pid:", p.pid


class ConsoleOutputCollector:
    '''
    Create a console window and start a process. Collect the logs generated by the process.
    '''
    normal_priority_tasks = ["webserver-cgi", "startBeanstalkd.bat", "mongodb.bat", "cherrypyServerV4",
                             "monitorServiceV2"]

    def __init__(self, log_root_path=None):
        self.log_collector_thread_list = []
        self.pList = []
        self.stopped = False
        self.log_root_path = log_root_path

    def runConsoleApp(self, target, cwd, progAndParam):
        checkExistPath = progAndParam
        if type(checkExistPath) == list:
            checkExistPath = checkExistPath[0]
            if not os.path.exists(checkExistPath):
                #Do not execute if the file does not exist
                return
        self.cwd = cwd
        if not (os.path.exists(self.cwd)):
            print 'execution path does not exist: ', self.cwd
        self.progAndParm = progAndParam

        try:
            target.set_title(str(progAndParam))
        except:
            traceback.print_exc()
            print "set title not supported"
            #print target
        #print '-------------------------',progAndParam
        #print cwd
        #self.prog = ['D:\\cygwin\\bin\\ls.exe','-l']
        ext = os.path.splitext(checkExistPath)[1]
        #print 'ext is:', ext
        pythonWinPathList = []
        try:
            pythonWinPathList.append(os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts/pythonw.exe'))
            #print 'using virtual env:', pythonWinPathList[0], progAndParam
        except:
            pass
        if ".py" == ext:
            pythonWinPathList.extend(['c:/Python27/pythonw.exe', 'd:/python27/pythonw.exe', 'd:/python25/pythonw.exe',
                                      'c:/python27/pythonw.exe', 'c:/python26/pythonw.exe', 'c:/python25/pythonw.exe'])
            for i in pythonWinPathList:
                if os.path.exists(i):
                    targetPythonExePath = i
                    break
                else:
                    #print i, ", does not exist"
                    pass
            self.prog = [targetPythonExePath, '-u']
            self.prog.extend(progAndParam)#Param 2 is the app
        else:
            self.prog = []
            self.prog.extend(progAndParam)

        #print self.prog
        #self.SetTitle(progAndParam[0])
        if True:#try:
            #print self.prog
            if not os.path.exists(self.prog[0]):
                print "path does not exist: ", self.prog[0]
            p = subprocess.Popen(self.prog, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0,
                                 creationflags=CREATE_NO_WINDOW)
            self.pList.append(p)
            #print "created pid:", p.pid

            find_flag = False
            for z in self.normal_priority_tasks:
                if progAndParam[0].find(z) != -1:
                    #Need normal priority for this app
                    find_flag = True
            if not find_flag:
                sysprocess.set_priority(p.pid, 1)
                pass
                #print "setting pid: %d, %s to below normal priority"%(p.pid, progAndParam[0])
            else:
                #print "pid: %d, %s use normal priority"%(p.pid, progAndParam[0])
                pass
                #print 'taskid:%d, pid:%d'%(int(p._handle), int(p.pid))

            log_path_base_name = os.path.basename(progAndParam[0])# + str(progAndParam[1:])
            normal_log_path = logDir.logDir(log_path_base_name + "_normal")
            err_log_path = logDir.logDir(log_path_base_name + "_error")
            thr1 = taskConsoleThread(target, p.stdout, progAndParam[0], False, normal_log_path.getLogFilePath())
            thr1.start()
            self.log_collector_thread_list.append(thr1)
            thr2 = taskConsoleThread(target, p.stderr, progAndParam[0], True, err_log_path.getLogFilePath())
            thr2.start()
            self.log_collector_thread_list.append(thr2)
            #print 'launch ok'
        else:#except:
            print 'launch exception'
            #self.appStarted = True

    def kill_console_process_tree(self):
        import win32api
        # TODO: do we need to kill applications?
        for i in self.pList:
            print 'processing:', i.pid, ", handle: ", int(i._handle)
            #print "cmd:", self.progAndParm
            sysprocess.killChildProcessTree(i.pid)
            try:
                win32api.TerminateProcess(int(i._handle), -1)
            except pywintypes.error:
                print "killing failed, app may terminated by itself: ", i.pid

        for i in self.log_collector_thread_list:
            i.quit()

    def send_stop_signal(self):
        pass