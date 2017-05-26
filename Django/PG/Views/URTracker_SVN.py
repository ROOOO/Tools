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
    cfg = CSettings(os.path.join(BASE_URL, 'Web', 'PG', CfgFilePath)).Json()
    # db = CDBSqlite(os.path.join(BASE_URL, 'Django', 'PG', 'db.sqlite3'))
    db = CDBPostgresql('tools', 'king', 'wqlwqlwql', '108.61.200.192')

    testingList = []
    db.cursor.execute('select distinct url, title from XXSY_URTracker where state = \'产品验证\';')
    try:
        testingList = db.cursor.fetchall()
    except:
        pass
    modifyingList = []
    db.cursor.execute('select distinct url, title from XXSY_URTracker where state = \'修改中\';')
    try:
        modifyingList = db.cursor.fetchall()
    except:
        pass

    blackList = []
    db.cursor.execute('select revision, author, svnDate, log from XXSY_SVNLog where author != \'xpc\' and revision >= ' + str(cfg['Min']) + ' and revision not in (select revision from XXSY_URTracker);')
    try:
        blackList = db.cursor.fetchall()
    except:
        pass

    wrongList = []
    db.cursor.execute('select revision, url from XXSY_URTracker where revision not in (select revision from XXSY_SVNLog) or revision > (select max(revision) from XXSY_SVNLog) or revision < ' + str(cfg['Min']) + ';')
    try:
        wrongList = db.cursor.fetchall()
    except:
        pass
    todoList = []
    db.cursor.execute('select distinct revision, task, url from XXSY_URTracker where state = \'等待制作版本\' order by revision;')
    try:
        todoList = db.cursor.fetchall()
    except:
        pass

    todoListTask = []
    for item in todoList:
        for task in str(item[1]).split(';'):
            if task not in todoListTask:
                todoListTask.append(task)
    todoListTask.sort()

    modTime = 0
    db.cursor.execute('select value from xxsy_misc where id = 1;')
    try:
        modTime = db.cursor.fetchall()[0][0]
    except:
        pass

    db.Close()
    
    rsp = {}
    rsp['title'] = cfg['Web']['Title']
    rsp['testingList'] = testingList
    rsp['modifyingList'] = modifyingList
    rsp['blackList'] = blackList
    rsp['wrongList'] = wrongList
    rsp['modTime'] = modTime
    rsp['todoList'] = todoList
    rsp['todoListTask'] = '\t'.join(todoListTask)

    return render_to_response('URTracker_SVN.html', rsp)
