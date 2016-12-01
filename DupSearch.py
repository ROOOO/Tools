#coding: utf-8

import os
import hashlib
import datetime
import time
import shutil
import platform
import re

class CFile:
    def __init__(self, path, name, size, postFix):
        self.path = path
        self.name = name
        self.size = size
        self.postFix = postFix
        self.md5 = ''

class DuplicatedSearch:
    def __init__(self, path = 'D:\\XMZ\\client\\bo201\\Assets'):
        self.path = path 
        self.files = {}
        self.md5s = {}
        self.dups = {}
        self.count = 0

    def searchAllFiles(self):
        for dirPath, dirNames, fileNames in os.walk(self.path):
            for fileName in fileNames:
                post = os.path.splitext(fileName)[1]
                if post != '.meta':
                    self.count += 1
                    path = os.path.join(dirPath, fileName)
                    size = os.path.getsize(path)
                    if not self.files.has_key(size):
                        self.files[size] = []
                    self.files[size].append(CFile(path, fileName, size, post))

    def searchDups(self):
        for size in self.files:
            if len(self.files[size]) > 1:
                for file in self.files[size]:
                    md5 = hashlib.md5(open(file.path, 'rb').read()).hexdigest()
                    if not self.md5s.has_key(md5):
                        self.md5s[md5] = []
                    file.md5 = md5
                    self.md5s[md5].append(file)

    def output(self, fileName = 'dup.txt', path = '', r = 0):
        txtFile = open(os.path.join(path, fileName), 'w+')
        txtFile.write('md5\tPath\tFileName\tPostFix\tSizeofFile\n')
        txtFile.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n')
        txtFile.write(str(r) + '\n')
        for md5 in self.md5s:
            if len(self.md5s[md5]) > 1:
                txtFile.write(md5 + '\n')
                for m in self.md5s[md5]:
                    txtFile.write(md5 + '\t' + m.path + '\t' + m.name + '\t' + m.postFix + '\t' + str(m.size) + '\n')
        txtFile.close()

    def djangoCheck(self, path = os.path.dirname(os.path.realpath(__file__)), r = 0):
        try:
            txtFile = open(os.path.join(path, 'dup.txt'), 'r+')
        except:
            f = ''
        else:
            f = txtFile.read()
            txtFile.close()
        found = re.findall(re.compile(r'(.*?)\n'), f)
        if len(found) > 0:
            if found[2] >= r:
                return
        self.searchAllFiles()
        self.searchDups()        
        self.output('dupCache.txt', path, r)
        shutil.copyfile(os.path.join(path, 'dupCache.txt'), os.path.join(path, 'dup.txt'))

    def check(self):
        t1 = datetime.datetime.now()
        self.searchAllFiles()
        self.searchDups()        
        self.output()
        t4 = datetime.datetime.now()
        print d.count
        print str(t4 - t1)

if __name__ == '__main__':
    sysstr = platform.system()
    if sysstr == 'Linux':
        d = DuplicatedSearch('/home/wangqinlei/xmz/bo2actapp/client/bo201/Assets')
        update = os.popen('cd /home/wangqinlei/xmz/bo2actapp/client/bo201/Assets && svn update').read()
        if re.search(r'svn cleanup', update):
            os.popen('cd /home/wangqinlei/xmz/bo2actapp/client/bo201/Assets && svn cleanup')
        r = re.findall(r'revision\s(\d+)', update)
        d.djangoCheck(r = r[0])
    else:
        d = DuplicatedSearch()
        d.djangoCheck()
