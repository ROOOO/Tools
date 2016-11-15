#coding: utf-8
from django.shortcuts import render, render_to_response

# Create your views here.

from django.http import HttpResponse, Http404
import os
import re
import sys
sys.path.append( os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from util.util import *
sys.path.pop(len(sys.path) - 1)

def URTracker_SVN_XXSY(request):
    xxsy_ss = CSystem()

    FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))))), 'Web', 'PG_OUTPUTS', 'xxsy_tracker_svn.txt')

    with open(FILE, 'r+') as file:
        svns = file.read()

    rst = []
    for svn in re.findall(re.compile(r'(.*?)eol', re.S), svns):
        rst.append(svn)

    rsp = {}
    rsp['svns'] = rst
    rsp['modTime'] = xxsy_ss.StrfTime(xxsy_ss.GetFileTime('m', FILE))


    return render_to_response('xxsy.html', rsp)
