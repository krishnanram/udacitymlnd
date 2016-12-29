import unittest
import ConfigParser
from Util import *

config = ConfigParser.RawConfigParser()
print getConfigDir()
config.read(getConfigDir() + "/Config.properties")

def getProperty(name) :
    return config.get('DatabaseSection', name);


def getPath(name) :
    print "KKKK,", getAppDir(), getProperty(name)
    return  getAppDir() + "/" + getProperty(name) + "/"

if __name__ == '__main__':

    print getPath('database.dbname')
    print getPath('strategies.data.path')

