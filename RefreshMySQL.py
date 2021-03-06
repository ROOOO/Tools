#coding: utf-8
import os
import sys
import re
import time
from util import util, settings

def r_e():
  u.runProcess('sh ' + os.path.join(s.getPath('serverTools'), 'update', 'home', 'r_e.sh'))
def r_s():
  u.runProcess('sh ' + os.path.join(s.getPath('serverTools'), 'update', 'home', 'r_s.sh'))
def reset():
  u.runProcess('sh ' + os.path.join(s.getPath('serverTools'), 'misc', 'resetdb.sh'))

if __name__ == '__main__':
  u = util()
  s = settings()
  if u.systemFlag() != 'Windows':
    print 'Only support Windows now.'
    exit()
  if len(sys.argv) <= 1:
    print 'At least one arg.\n'
    print '1 Daily Refresh.\n2 r_e.\n3 r_s.\n4 Reset database.\n'
    exit()

  u.runProcess('explorer.exe ' + s.getPath('server'))
  raw_input()
  f = os.path.join(s.getPath('server'), 'daily.txt')
  current = time.time()
  if sys.argv[1] == '1':
    u.killProcess(['node*', 'exebox*'])
    try:
      latest = round(float(u.readFile(f)), 3)
    except:
      latest = 0
    for dirPath, dirNames, fileNames in u.walkPath(os.path.join(s.getPath('server'), 'sql', 'home')):
      for fileName in fileNames:
        if re.match(r'fix', os.path.splitext(fileName)[0]):
          file = os.path.join(dirPath, fileName)
          t = round(u.getTime('m', file), 3)
          if latest < t:
            print s.getMySQLCMD(file)
            u.runProcess(s.getMySQLCMD(file))
    u.writeFile(f, str(current))
    r_s()
    r_e()
    # u.runProcess(os.path.join(s.getPath('serverTools'), 'ExeBox', 'ExeBox.exe'), True)
  elif sys.argv[1] == '2':
    r_e()
  elif sys.argv[1] == '3':
    r_s()
  elif sys.argv[1] == '4':
    u.killProcess(['node*', 'exebox*'])
    reset()
    u.writeFile(f, str(current))
