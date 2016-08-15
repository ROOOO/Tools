#coding: utf-8
import os
import sys
from util import util

if __name__ == '__main__':
  u = util()
  if u.systemFlag() != 'Windows':
    print 'Only support Windows now.'
    exit()
  if len(sys.argv) <= 1:
    print 'At least one task name.'
    exit()
  tasks = sys.argv
  if sys.argv[1] == '1':
    tasks = ['conhost*', 'powershell*']
  u.killProcess(tasks)
