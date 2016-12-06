#coding: utf-8
__author__ = 'King'

import os
import re
import sys
import datetime
import time
import platform

class Items:
    def __init__(self, file, line = '', lineNum = 0, author = '', revision = 0):
        self.file = file
        self.line = line
        self.lineNum = lineNum
        self.author = author
        self.revision = revision

class FindChinese:
    def __init__(self, svnPath, p = False, localPath = '', justLocal = False):
        self.svnPath = svnPath
        self.localPath = localPath
        self.files = []
        self.Items = []
        self.comment = False
        self.prt = p
        self.justLocal = justLocal
        self.singleFile = False
        if self.svnPath == '1':
            self.singleFile = True  
            self.justLocal = True

    def searchAll(self, path, postFix):
        rst = os.popen('svn ls ' + path).read()
        files = re.findall(re.compile(r'(.*?\.' + postFix + ')\n'), rst)
        for file in files:
            if len(file) != 0:
                if not re.search(re.compile(r'GemUIPanel'), file):
                    self.files.append(path + file)
        folders = re.findall(re.compile(r'(.*/)'), rst)
        for folder in folders:
            if len(folder) != 0:
                self.searchAll(path + folder, postFix)

    def LocalSearch(self, path, postFix):
        for dirPath, dirNames, fileNames in os.walk(path):
            lastFile = ''
            for fileName in fileNames:
                curFile = fileName
                if curFile != lastFile:
                    self.comment = False
                    lastFile = curFile
                if os.path.splitext(fileName)[1] == '.' + postFix:
                    file = os.path.join(dirPath, fileName)
                    fread = os.popen('cat -n "' + file + '"').read()
                    lines = re.findall(r'\d+\s+(.*?)\n', fread) 
                    if postFix == 'bytes':
                        for line in lines:
                            if self.findLuaChinese(line):
                                self.files.append(file)
                                break
                    elif postFix == 'prefab':
                        for line in lines:
                            if self.findPrefabChinese(line):
                                self.files.append(file)
                                break

    def searchSVNFiles(self):
        if self.singleFile:
            self.files.append(self.localPath)
            return
        if self.localPath != '':
            self.LocalSearch(os.path.join(self.localPath, 'Lua'), 'bytes')
            self.LocalSearch(os.path.join(self.localPath, 'Ui'), 'prefab')
            return
        folders = os.popen('svn ls ' + self.svnPath).read()
        if 'Lua/' in folders:
            self.searchAll(self.svnPath + 'Lua/', 'bytes')
        if 'Ui/' in folders:
            self.searchAll(self.svnPath + 'Ui/', 'prefab')

    def findLuaChinese(self, line):
        # print line
        try:
            words = unicode(line, 'utf-8')
        except:
            words = line
        comment = False
        count = 0
        count2 = 0
        count3 = 0
        for word in words:
            # print word
            # --[[[[
            if comment and word == '[':
                if count2 == 0:
                    count2 = count
                count2 += 1
                if count2 == 4:
                    self.comment = True
                    return False
                else:
                    continue
            # -- || --[
            elif comment:
                return False

            if self.comment and word != u']' and count3 == 0:
                return False
            if self.comment and word == u']':
                count3 += 1
                continue
            if self.comment and count3 >= 2:
                if word == ']':
                    pass
                elif word != '-':
                    count3 = 0
                else:
                    count3 += 1
                    if count3 == 3:
                        continue
            if self.comment and count3 == 4:
                self.comment = False
                return False

            if word == '-':
                count += 1
                if count == 2:
                    comment = True
                    continue
                else:
                    continue
            if word > u'\u4e00' and word != u'\ufeff':
                return True

        return False

    def findPrefabChinese(self, line):
        if re.search(re.compile(r'mText:'), line):
            words = re.findall(re.compile(r'\\u(\S{4})'), line)
            for word in words:
                if word > u'4e00':
                    return True
        return False

    def readFiles(self):
        i = 0
        l = len(self.files)
        start_time = time.time()
        rt1 = start_time
        for file in self.files:
            if self.prt:
                print '                                                READING ' + file.split(os.sep)[-1] + ' ...' 
            if not self.justLocal:
                txt = os.popen('svn blame ' + file + ' | cat -n').read()
                lines = re.findall(r'(\d+)\s+(\d+)\s+(\w+)\s+(.*?)\n', txt)
            else:
                txt = os.popen('cat -n ' + file).read()
                lines = re.findall(r'(\d+)\s+(.*?)\n', txt)
            for line in lines:
                if (not self.justLocal and line[3] != ''):
                    self.Items.append(Items(file, line[3], line[0], line[2], line[1]))
                elif (self.justLocal and line[1] != ''):
                    self.Items.append(Items(file, line[1], line[0], ''))
            i += 1
            rt2 = time.time()
            if self.prt:
                print ('%.3f' % (rt2 - rt1)) + 's', '%.3f' % ((time.time() - start_time) / i * (l - i)) + 's', '%.2f' % float(float(i) / l * 100) + '%', str(i) + '/' + str(l), file
            rt1 = rt2

    def go(self, fileName = 'Chinese.txt', path = '', r = 0):
        txtFile = open(os.path.join(path, fileName), 'w+')
        txtFile.write('author\tfile\tFile\'s Name\tlineNum\tPrefab/Lua\n')
        txtFile.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n')
        txtFile.write(str(r) + '\n')
        lastFile = ''
        for item in self.Items:
            curFile = item.file
            if curFile != lastFile:
                self.comment = False
                lastFile = curFile
            if (re.search(re.compile(r'\.bytes'), item.file) and self.findLuaChinese(item.line)) or (re.search(re.compile(r'\.prefab'), item.file) and self.findPrefabChinese(item.line)):
                if self.singleFile:
                    print str(item.lineNum)
                    continue
                if re.search(re.compile(r'\.bytes'), item.file):
                    txtFile.write(item.author + '\t' + item.file + '\t' + item.file.split(os.sep)[-1] + '\t' + str(item.lineNum) + '\tLua\n')
                else:
                    txtFile.write(item.author + '\t' + item.file + '\t' + item.file.split(os.sep)[-1] + '\t' + str(item.lineNum) + '\tPrefab\n')
        txtFile.close()

    def Check(self, path = os.path.dirname(os.path.realpath(__file__)), r = 0):
        try:
            txtFile = open(os.path.join(path, 'Chinese.txt'), 'r+')
        except:
            f = ''
        else:
            f = txtFile.read()
            txtFile.close()
        found = re.findall(re.compile(r'(.*?)\n'), f)
        if len(found) > 0 and not self.singleFile:
            if found[2] >= r:
                return
        t1 = datetime.datetime.now()
        self.searchSVNFiles()
        t2 = datetime.datetime.now()
        self.readFiles()
        t3 = datetime.datetime.now()
        self.go(path = path, r = r)
        t4 = datetime.datetime.now()
        if self.prt:
            print '文件总数' + str(len(self.files))
            print 'svn ls 耗时' + str(t2 - t1)
            print 'svn blame 耗时' + str(t3 - t2)
            print '检索中文耗时' + str(t4 - t3)
            print '总耗时' + str(t4 - t1)

if __name__ == '__main__':
    sysstr = platform.system()
    p = False
    svn = 'svn://bigsvr/bo2actapp/client/bo201/Assets/Resources/'
    if sysstr == 'Linux':
        local = '/home/wangqinlei/xmz/bo2actapp/client/bo201/Assets/Resources/'
    else:
        local = 'D:\\XMZ\\client\\bo201\\Assets\\Resources'
    justLocal = False

    if len(sys.argv) == 3:
        p = True
        svn = sys.argv[1]
        local = sys.argv[2]
    elif len(sys.argv) == 2 and sys.argv[1] != '1':
        p = True
        local = sys.argv[1]
    elif len(sys.argv) == 2 and sys.argv[1] == '1':
        p = True
        justLocal = True

    if sysstr == 'Linux':
        update = os.popen('cd /home/wangqinlei/xmz/bo2actapp/client/bo201/Assets && svn revert -R . && svn update').read()
        r = re.findall(r'revision\s(\d+)', update)
        f = FindChinese(svn, p, local, justLocal)
        f.Check(os.path.dirname(os.path.realpath(__file__)), r[0])
    else:
        f = FindChinese(svn, True, local, justLocal)
        f.Check()

