#coding: utf-8

import re
import sys
sys.path.append('../..')
from util.util import *
sys.path.pop(len(sys.path) - 1)

class CPGTracker:
  def __init__(self, CfgFilePath):
    self.Settings = CSettings(CfgFilePath).Json()
    self.__ss = CSystem()
    self.__selfSettings = CSettings('PG.json').Json()
    self.__Web = CWeb(self.Settings)
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
    self.__Web.WaitUntil('text_to_be_present_in_element', self.__selfSettings['Buttons']['Sort']['By'], self.__selfSettings['Buttons']['Sort']['Arg'], ' ')
    self.__Web.ExecScript("javascript:__doPostBack('ctl00$CP1$gvProblems','Sort$Text1')")
    if self.Settings['Driver']['use'] == 2:
      self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['SortIcon']['By'], self.__selfSettings['Buttons']['SortIcon']['Arg'])
    else:
      self.__ss.Sleep(1)
      self.__Web.WaitUntil('invisibility_of_element_located', self.__selfSettings['Buttons']['WaitingPanel']['By'], self.__selfSettings['Buttons']['WaitingPanel']['Arg'])

  def __RegRevisions(self, src, on, off):
    src = re.sub(re.compile(r'&nbsp;'), '', src)
    pattern1 = re.compile(self.Settings['RegExp']['Revisions']['Re'], re.S)
    items = re.findall(pattern1, src)
    pattern2 = re.compile(r',|，')
    b = False
    for item in items:
      if item[2] == '' or item[2] == ' ' or item[2] == u'\xa0':
        continue
      if item[1] in self.Settings['RegExp']['Revisions']['States_On']:
        for x in re.split(pattern2, item[2]):
          if x not in on:
            on.append(x)
            b = True
      elif item[1] in self.Settings['RegExp']['Revisions']['States_Off']:
        for x in re.split(pattern2, item[2]):
          if x not in off and x >= self.Settings['Min']:
            off.append(x)
    return b

  def GetRevisions(self):
    HTMLs = []
    HTMLs.append(self.__Web.GetPageSource())
    pageIdx = 2
    numIdx = 2
    on = []
    off = []
    while pageIdx <= self.__PageNum:
      self.__Web.ExecScript('javascript:__doPostBack(\'ctl00$CP1$gvProblems\',\'Page$' + str(pageIdx) + '\')')
      if numIdx > 10:
        numIdx = 8
      if not self.__RegRevisions(HTMLs[pageIdx - 2], on, off):
        break
      self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['NumberSelected']['By'], self.__selfSettings['Buttons']['NumberSelected']['Arg'][0] + str(pageIdx) + self.__selfSettings['Buttons']['NumberSelected']['Arg'][1])
      HTMLs.append(self.__Web.GetPageSource())
      pageIdx += 1
      numIdx += 1
    self.__RegRevisions(HTMLs[pageIdx - 2], on, off)
    return [on, off]

  def URTrackerCheck(self, args):
    # try:
    self.__Login()
    self.__GoToBranchPage(args['URTracker_Branch'])
    self.__PageNum = self.__GetBranchPageNum()
    self.__SortPage()
    return self.GetRevisions()
    # except:
    #   self.__Web.Quit()
    #   print 'err'

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
    pattern = re.compile(self.Settings['RegExp']['SVN']['Re'], re.S)
    items = re.findall(pattern, self.__logs)
    for item in items:
      self.__logItems[item[0]] = SVNItem(item[0], item[1], item[2], item[3])

  def CheckLogs(self, revisions):
    blackList = []
    for logId in self.__logItems:
      if logId not in revisions:
        blackList.append(self.__logItems[logId])
    return blackList
