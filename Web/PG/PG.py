#coding: utf-8

import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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

  def __RegRevisions(self, src, on, off, todo, _min, _max):
    src = re.sub(re.compile(r'&nbsp;'), '', src)
    pattern1 = re.compile(self.Settings['RegExp']['Revisions']['Re'], re.S)
    items = re.findall(pattern1, src)
    pattern2 = re.compile(r',|，')
    b = False
    for item in items:
      if item[2] == '' or item[2] == ' ' or item[2] == u'\xa0':
        continue
      revisions_s = re.split(pattern2, item[2])
      if item[1] in self.Settings['RegExp']['Revisions']['States_On']:
        for r in revisions_s:
          if not on.has_key(r):
            on[r] = STrackerItem({
              'url' : item[0],
              'state' : item[1],
              'revisions' : item[2],
              }) 
      elif item[1] in self.Settings['RegExp']['Revisions']['States_Off']:
        for r in revisions_s:
          if not off.has_key(r):
            off[r] = STrackerItem({
              'url' : item[0],
              'state' : item[1],
              'revisions' : item[2],
              }) 
      if item[1] in self.Settings['RegExp']['Revisions']['States_Todo']:
        for r in revisions_s:
          if r not in todo:
            todo.append(r)

        _min[0] = min(revisions_s) if min(revisions_s) < _min[0] or _min[0] == 0 else _min[0]
        _max[0] = max(revisions_s) if max(revisions_s) > _max[0] or _max[0] == 0 else _max[0]
        b = True
    return b

  def GetRevisions(self):
    HTMLs = []
    HTMLs.append(self.__Web.GetPageSource())
    pageIdx = 2
    numIdx = 2
    on = {}
    off = {}
    todo = []
    _min = [0]
    _max = [0]
    while pageIdx <= self.__PageNum:
      self.__Web.ExecScript('javascript:__doPostBack(\'ctl00$CP1$gvProblems\',\'Page$' + str(pageIdx) + '\')')
      if numIdx > 10:
        numIdx = 8
      if not self.__RegRevisions(HTMLs[pageIdx - 2], on, off, todo, _min, _max):
        break
      self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['NumberSelected']['By'], self.__selfSettings['Buttons']['NumberSelected']['Arg'][0] + str(pageIdx) + self.__selfSettings['Buttons']['NumberSelected']['Arg'][1])
      HTMLs.append(self.__Web.GetPageSource())
      pageIdx += 1
      numIdx += 1
    self.__RegRevisions(HTMLs[pageIdx - 2], on, off, todo, _min, _max)
    self.__Web.Quit()
    return on, off, todo, _min[0], _max[0]

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
