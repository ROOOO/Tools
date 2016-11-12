# -*- coding: utf-8 -*-
__author__ = 'King'

import os
import sys
import re
from util import util

class Log:
    def __init__(self, name = ''):
        self.util = util()
        self.svnPath = 'svn://bigsvr/bo2actapp/'
        self.logs = []
        self.name = name

    def GetLog(self):
        log = self.util.runProcess('svn log ' + self.svnPath + ' -r {2016-07-01}:{2016-09-30}', True)
        pattern = re.compile(r'r\d+.\|.(\w+)\s\|.(\d+-\d+-\d+)\s.*?\d+.(lines|line)\n\n(.*?)\n', re.S)
        self.logs = re.findall(pattern, log)
        self.SearchLogs()

    def SearchLogs(self):
        rst = {}
        for log in self.logs:
            if log[0] == self.name:
                if not rst.has_key(log[1]):
                    rst[log[1]] = []
                if not log[3] in rst[log[1]]:
                    rst[log[1]].append(log[3])
        self.logs = rst
        self.BetterLogs()

    def BetterLogs(self):
        self.logs = sorted(self.logs.iteritems(), key = lambda d:d[0])
        self.WriteFile()

    def WriteFile(self):
        file = open('SvnLogs\\' + self.name + 'SvnLog.txt', 'w+')
        for date, logs in self.logs:
            file.write('# ' + date + '\n')
            idx = 1
            for log in logs:
                if log != '' and not (re.match(r'Merged revision', log)  or (re.match(r'合并了', log))):
                    file.write(' ' + str(idx) + '. ' + log.decode('gb2312').encode('utf-8') + '\n')
                    idx += 1
            file.write('\n')

        file.close()

if __name__ == '__main__':
    members = ['chensiyuan', 'wangqinlei', 'gedamis', 'zhangzhiyang', 'chenweiwei', 'lengbing', 'wangxiao', 'zhangbinglei']
    for member in members:
        L = Log(member)
        L.GetLog()
        print member
