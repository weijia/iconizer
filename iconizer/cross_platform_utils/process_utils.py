

class CrossPlatformProcessUtils(object):
    normal_priority_tasks = ["webserver-cgi",
                             "startBeanstalkd.bat",
                             "mongodb.bat",
                             "cherrypyServerV4",
                             "monitorServiceV2"
                             ]

    def update_process_priority(self, app_or_script_path_and_param_list, p):
        try:
            from iconizer.win import sysprocess
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
        except:
            pass

    def kill_process(self, process):
        try:
            from iconizer.win import sysprocess
            print 'processing:', process.pid, ", handle: ", int(process._handle)
            sysprocess.killChildProcessTree(process.pid)
            sysprocess.TerminateProcess(process)
        except:
            process.kill()