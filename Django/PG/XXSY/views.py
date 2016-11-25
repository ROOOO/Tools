#coding: utf-8
from django.shortcuts import render, render_to_response, redirect

# Create your views here.

from django.http import HttpResponse, Http404
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Views.URTracker_SVN import URTracker_SVN
sys.path.pop(len(sys.path) - 1)

def URTracker_SVN_XXSY(request):
    return URTracker_SVN(request, 'xxsy_tracker_svn.txt', 'XXSY.json')
