#coding: utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.util import *

if __name__ == '__main__':
  u = CSystem()
  sysFlag = u.GetSystemFlag()
  if len(sys.argv) <= 1:
    print 'At least one task name.'
    exit()

  tasks = sys.argv
  if sys.argv[1] == '1':
    s = CSettings('TaskKill.json')
    tasks = []
    for task in s.Json()['Default']:
      tasks.append(s.Json()['Default'][task])

  u.KillProcess(tasks)
