#coding: utf-8
from django.shortcuts import render, render_to_response, redirect

# Create your views here.

from django.http import HttpResponse, Http404
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from util.util import *
sys.path.pop(len(sys.path) - 1)

def URTracker_SVN(request, template, logFile):
    xxsy_ss = CSystem()

    FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))))), 'Web', 'PG_OUTPUTS', logFile)

    with open(FILE, 'r+') as file:
        svns = file.read()

    testingList = []
    for svn in re.findall(re.compile(r'(.*?)\t(.*?)\ttesting\n'), svns):
        testingList.append({
            'url' : svn[0],
            'title' : svn[1],
            })
    blackList = []
    for svn in re.findall(re.compile(r'black\t(.*?)\t"""(.*?)"""\tblack\n', re.S), svns):
        blackList.append({
            'info' : svn[0],
            'log' : svn[1],
            })
    wrongList = []
    for svn in re.findall(re.compile(r'(.*?)\t(.*?)\twrong\n'), svns):
        wrongList.append({
            'revision' : svn[0],
            'url' : svn[1],
            })
    todoList = []
    for svn in re.findall(re.compile(r'(\d+),', re.S), svns):
        todoList.append(svn)

    rsp = {}
    rsp['testingList'] = testingList
    rsp['blackList'] = blackList
    rsp['wrongList'] = wrongList
    rsp['modTime'] = xxsy_ss.StrfTime(xxsy_ss.GetFileTime('m', FILE) + 8 * 60 * 60)
    rsp['todo'] = ', '.join(todoList)
    rsp['count'] = len(todoList)

    return render_to_response(template, rsp)