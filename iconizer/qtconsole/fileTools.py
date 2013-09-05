#import os
from pkg_resources import Requirement, resource_filename, resource_exists


def find_resource_in_pkg(filename):
    '''
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            #print 'find file:', os.path.join(dirpath, filename)
            return os.path.join(dirpath, filename)
    '''
    generated_path = resource_filename(Requirement.parse("iconizer"), "iconizer/qtconsole/%s" % filename)
    print generated_path
    if resource_exists(Requirement.parse("iconizer"), "iconizer/qtconsole/%s" % filename):
        return resource_filename(Requirement.parse("iconizer"), "iconizer/qtconsole/%s" % filename)
    print filename, "not found"
    raise "file not found"
    return None
