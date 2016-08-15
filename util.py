#coding: utf-8
import os
import time
import platform
import subprocess

class settings:
    def __init__(self):
        self.projectPath = ''
        self.serverFilesPath = 'D:\\XMZ\\bo2_svr\\svr\\'
        self.serverToosPath = 'D:\\XMZ\\bo2_svr\\tools\\'
        self.mySQL = 'mysql -h192.168.6.55 -uroot -ppixeldb2015 -Dxmz_homeKing < '

    def getPath(self, name):
        if name == 'project':
            return self.projectPath
        elif name == 'server':
            return self.serverFilesPath
        elif name == 'serverTools':
            return self.serverToosPath

    def getMySQLCMD(self):
        return self.mySQL

class util:
    def __init__(self):
        pass

    def systemFlag(self):
        return platform.system()

    def walkPath(self, path):
        if path == '':
            print 'Error path'
            return
        # dirPath, dirNames, fileNames
        return os.walk(path)

    def getTime(self, cm, filePath):
        if cm == 'c':
            return os.path.getctime(filePath)
        elif cm == 'm':
            return os.path.getmtime(filePath)

    def writeFile(self, filePath, blocks):
        file = open(filePath, 'w+')
        file.write(blocks)
        file.close()

    def readFile(self, filePath):
        file = open(filePath, 'r+')
        text = file.read()
        file.close()
        return text

    def killProcess(self, names):
        if not isinstance(names, list):
            print 'Arg 2 must be a list'
            return
        for name in names:
            print name
            subprocess.call('taskkill /f /im ' + name, shell = False)

    def runProcess(self, path, usepopen = False):
        if usepopen:
            return os.popen(path).read()
        subprocess.call(path, shell = False)
