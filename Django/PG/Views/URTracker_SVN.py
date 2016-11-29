#coding: utf-8
from django.shortcuts import render, render_to_response, redirect

# Create your views here.

from django.http import HttpResponse, Http404
import os
import re
import sys
BASE_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(BASE_URL)
from util.util import *
sys.path.pop(len(sys.path) - 1)

def URTracker_SVN(request, CfgFilePath):
    ss = CSystem()
    cfg = CSettings(os.path.join(BASE_URL, 'Web', 'PG', CfgFilePath)).Json()
    db = CDBSqlite(os.path.join(BASE_URL, 'Django', 'PG', 'db.sqlite3'))

    testingList = []
    testingList = db.cursor.execute('select url, title from XXSY_URTracker where state == "分支验证";').fetchall()

    blackList = []
    blackList = db.cursor.execute('select revision, author, svnDate, log from XXSY_SVNLog where revision not in (select revision from XXSY_URTracker);').fetchall()

    wrongList = []
    wrongList = db.cursor.execute('select revision, url from XXSY_URTracker where revision not in (select revision from XXSY_SVNLog) and revision >= (select max(revision) from XXSY_SVNLog);').fetchall()

    todoList = []
    todoList = db.cursor.execute('select revision, task from XXSY_URTracker where state == "等待交付运营商";').fetchall()

    todoListTask = []
    for item in todoList:
        for task in str(item[1]).split(';'):
            if task not in todoListTask:
                todoListTask.append(task)
    todoListTask.sort()
    
    rsp = {}
    rsp['title'] = cfg['Web']['Title']
    rsp['testingList'] = testingList
    rsp['blackList'] = blackList
    rsp['wrongList'] = wrongList
    # rsp['modTime'] = ss.StrfTime(ss.GetFileTime('m', FILE) + 8 * 60 * 60)
    rsp['todoList'] = todoList
    rsp['todoListTask'] = '\t'.join(todoListTask)

    return render_to_response('URTracker_SVN.html', rsp)
