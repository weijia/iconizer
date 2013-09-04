import os
import random
import time


def getFreeName(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext + ext):
        path_without_ext += '-' + str(random.randint(0, 10))
        #print thumb_path_without_ext
    return path_without_ext + ext


def getTimestampWithFreeName(path, ext, prefix=''):
    """
    Return a unused filename according to current time.
    :param path:
    :param ext: should start with "."
    :param prefix:
    :return:
    """
    #print path, ext, prefix
    filename = unicode(prefix + str(time.time()))
    return getFreeName(path, filename, ext)


def ensure_dir(fullPath):
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)


class logDir:
    def __init__(self, logName, logRootPath=None, maxLogFile=10):
        if logRootPath is None:
            logRootPath = os.getcwd()
        self.logName = logName.replace("\\", "_").replace("/", "_").replace(":", "_"). \
            replace("'", "").replace('"', "").replace("?", "").replace("*", "").replace(" ", "")
        self.logFullPath = os.path.join(logRootPath, self.logName)
        self.maxLogFile = maxLogFile
        ensure_dir(self.logFullPath)

    def getLogFilePath(self):
        fileList = {}
        numberList = []
        for i in os.listdir(self.logFullPath):
            try:
                number = float(i.replace(".log", ""))
            except:
                continue
            fileList[number] = i
            numberList.append(number)
        numberList.sort()
        #print numberList
        deleteLen = len(numberList) - self.maxLogFile
        #print deleteLen
        if deleteLen >= 0:
            #Delete old ones
            for i in numberList[0:deleteLen + 1]:
                #print 'deleting:', i
                try:
                    os.remove(os.path.join(self.logFullPath, fileList[i]))
                except WindowsError:
                    pass
        return getTimestampWithFreeName(self.logFullPath, '.log')


if __name__ == '__main__':
    l = logDir("testLogDir")
    f = open(l.getLogFilePath(), 'w')
    f.close()