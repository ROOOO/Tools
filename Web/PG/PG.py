#coding: utf-8

import re
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJ_DIR)
from util.util import *
sys.path.pop(len(sys.path) - 1)

class STrackerItem:
  def __init__(self, args):
    self.url = args['url'] if args['url'] else ''
    self.state = args['state'] if args['state'] else ''
    self.revisions = args['revisions'] if args['revisions'] else []

class CPGTracker:
  def __init__(self, CfgFilePath):
    self.Settings = CSettings(CfgFilePath).Json()
    self.__ss = CSystem()
    self.__selfSettings = CSettings('PG.json').Json()
    self.__Web = CWeb(self.Settings, '', self.Settings['Cookie'])
    self.__Element = CWebElement(self.__Web.GetDriver())
    self.__PageNum = 0
    self.__CfgFilePath = CfgFilePath
    self.__db = CDBSqlite(os.path.join(PROJ_DIR, 'Django', 'PG', 'db.sqlite3'))
    self.__compress = CCompress()

  def __Login(self):
    self.__Web.Goto(self.__selfSettings['URTracker']['Login'])
    key1Element = self.__Element.Find('name', 'txtEmail').SendKeys(self.__selfSettings['UserInfo']['Key1'])
    key2Element = self.__Element.Find('name', 'txtPassword').SendKeys(self.__selfSettings['UserInfo']['Key2']).SendKeys(self.__Element.Keys('RETURN'))

  def __GoToBranchPage(self, url):
    self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['Project']['By'], self.__selfSettings['Buttons']['Project']['Arg'])
    self.__Web.Goto(url)
    self.__Web.WaitUntil('element_to_be_clickable', self.Settings['Buttons']['Tracking']['By'], self.Settings['Buttons']['Tracking']['Arg'])[1].click()

  def __GetBranchPageNum(self):
    # 不管第二版面了，超过12只取12，连续有12页tracker需要查询也是厉害了... 那时候再加吧
    try:
      self.__Web.WaitUntil('presence_of_all_elements_located', self.__selfSettings['Buttons']['Number']['By'], self.__selfSettings['Buttons']['Number']['Arg'])
    except:
      return 1
    else:
      return self.__Element.Find(self.__selfSettings['Buttons']['Numbers']['By'], self.__selfSettings['Buttons']['Numbers']['Arg']).Count()

  def __SortPage(self):
    self.__Web.ExecScript("javascript:__doPostBack('ctl00$CP1$gvProblems','Sort$Text1')")
    self.__Web.WaitUntil('visibility_of_element_located', self.Settings['Buttons']['SortIconAsc']['By'], self.Settings['Buttons']['SortIconAsc']['Arg'])
    # self.__Web.WaitUntil('text_to_be_present_in_element', self.__selfSettings['Buttons']['Sort']['By'], self.__selfSettings['Buttons']['Sort']['Arg'], ' ')
    self.__Web.ExecScript("javascript:__doPostBack('ctl00$CP1$gvProblems','Sort$Text1')")
    # if self.Settings['Driver']['use'] == 2:
    self.__Web.WaitUntil('visibility_of_element_located', self.Settings['Buttons']['SortIconDesc']['By'], self.Settings['Buttons']['SortIconDesc']['Arg'])
    # else:
    #   self.__ss.Sleep(1)
    #   self.__Web.WaitUntil('invisibility_of_element_located', self.__selfSettings['Buttons']['WaitingPanel']['By'], self.__selfSettings['Buttons']['WaitingPanel']['Arg'])

  def __RegRevisions(self, src, lists):
    # on = lists[0]
    # off = lists[1]
    # todo = lists[2]
    # testing = lists[3]
    # _min = lists[4]
    # _max = lists[5]
    src = re.sub(re.compile(r'&nbsp;'), '', src)
    pattern1 = re.compile(self.Settings['RegExp']['Revisions']['Re'], re.S)
    items = re.findall(pattern1, src)
    pattern2 = re.compile(r',|，')
    b = False
    for item in items:
      if item[3] == '' or item[3] == ' ' or item[3] == u'\xa0':
        continue
      revisions_s = re.split(pattern2, item[3])
      # if item[2] in self.Settings['RegExp']['Revisions']['States_On']:
      print revisions_s
      for r in revisions_s:
        if self.__CfgFilePath == 'XXSY.json':
          self.__db.cursor.execute('insert into XXSY_xxsy_urtracker values (NULL, ?, ?, ?, ?);', (item[0], (item[2]), r, (item[4])))
          # if not on.has_key(r):
          #   on[r] = STrackerItem({
          #     'url' : item[0],
          #     'state' : item[2],
          #     'revisions' : item[3],
          #     }) 
      # elif item[2] in self.Settings['RegExp']['Revisions']['States_Off']:
      #   for r in revisions_s:
      #     if not off.has_key(r):
      #       off[r] = STrackerItem({
      #         'url' : item[0],
      #         'state' : item[2],
      #         'revisions' : item[3],
      #         })

      # if item[2] in self.Settings['RegExp']['Revisions']['States_NotEnd']: 
      #   _min[0] = min(revisions_s) if min(revisions_s) < _min[0] or _min[0] == 0 else _min[0]
      #   _max[0] = max(revisions_s) if max(revisions_s) > _max[0] or _max[0] == 0 else _max[0]
      #   b = True

      # if item[2] in self.Settings['RegExp']['Revisions']['States_Todo']:
      #   for r in revisions_s:
      #     if not todo.has_key(r):
      #       try:
      #         todo[r] = item[4]
      #       except:
      #         todo[r] = 'x'

      # if item[2] in self.Settings['RegExp']['Revisions']['States_Testing']:
      #   if not testing.has_key(item[0]):
      #     testing[item[0]] = item[1]
    self.__db.Commit()
    print self.__db.cursor.execute('select * from XXSY_xxsy_urtracker limit 5').fetchall()[0][2].encode('gbk')
    return b

  def GetRevisions(self):
    HTMLs = []
    HTMLs.append(self.__Web.GetPageSource())
    pageIdx = 2
    numIdx = 2
    lists = [
      # 'on' = {},
      # 'off' = {},
      # 'todo' = [],
      # 'testing' = [],
      # '_min' = [0],
      # '_max' = [0],
      {},
      {},
      {},
      {},
      [0],
      [0],
    ]
    while pageIdx <= self.__PageNum:
      self.__Web.ExecScript('javascript:__doPostBack(\'ctl00$CP1$gvProblems\',\'Page$' + str(pageIdx) + '\')')
      if numIdx > 10:
        numIdx = 8
      if not self.__RegRevisions(HTMLs[pageIdx - 2], lists):
        break
      self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['NumberSelected']['By'], self.__selfSettings['Buttons']['NumberSelected']['Arg'][0] + str(pageIdx) + self.__selfSettings['Buttons']['NumberSelected']['Arg'][1])
      HTMLs.append(self.__Web.GetPageSource())
      pageIdx += 1
      numIdx += 1
    self.__RegRevisions(HTMLs[pageIdx - 2], lists)
    self.__Web.Quit()
    return lists

  def URTrackerCheck(self, args):
    try:
      self.__Login()
      self.__GoToBranchPage(args['URTracker_Branch'])
      self.__PageNum = self.__GetBranchPageNum()
      self.__SortPage()
      return self.GetRevisions()
    except Exception, e:
      self.__Web.Quit()
      self.__ss.Traceback(Exception, e)      
      return {}, {}, {}, 0, 0

class SVNItem:
  def __init__(self, revision, author, time, log):
    self.revision = revision
    self.author = author
    self.time = time
    self.log = log

class CPGSVN:
  def __init__(self, CfgFilePath, rMin, rMax):
    # 降低耦合，多取一次文件吧
    self.Settings = CSettings(CfgFilePath).Json()
    self.__svnPath = self.Settings['SVNPath']['Branch']
    self.__rMin = rMin
    self.__rMax = rMax
    self.__ss = CSystem()
    self.__logs = ''
    self.__logItems = {}
    self.__GetLogs()

  def __GetLogs(self):
    self.__logs = self.__ss.RunProcess(u'svn log -r ' + str(self.__rMin) + ':' + str(self.__rMax) + ' ' + self.__svnPath, True)
    if self.__logs == '':
      self.__logs = self.__ss.RunProcess(u'svn log -r ' + str(self.__rMin) + ':' + 'HEAD' + ' ' + self.__svnPath, True)
    pattern = re.compile(self.Settings['RegExp']['SVN']['Re'], re.S)
    items = re.findall(pattern, self.__logs)
    print self.__rMax, self.__rMin
    for item in items:
      self.__logItems[item[0]] = SVNItem(item[0], item[1], item[2], item[3] if item[3] else '')

  def CheckLogs(self, revisions, todoRevisions):
    blackList = []
    wrongList = []
    for logId in self.__logItems:
      if logId not in revisions:
        blackList.append(self.__logItems[logId])
    for revision in todoRevisions:
      if not self.__logItems.has_key(revision):
        wrongList.append(revision)
    return [blackList, wrongList]
