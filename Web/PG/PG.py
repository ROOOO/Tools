#coding: utf-8

import re
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJ_DIR)
from util.util import *
sys.path.pop(len(sys.path) - 1)

class CPGTracker:
  def __init__(self, CfgFilePath):
    self.Settings = CSettings(CfgFilePath).Json()
    self.__ss = CSystem()
    self.__selfSettings = CSettings('PG.json').Json()
    self.__Web = CWeb(self.Settings, '', self.Settings['Cookie'])
    self.__Element = CWebElement(self.__Web.GetDriver())
    self.__PageNum = 0
    self.__CfgFilePath = CfgFilePath
    # self.__db = CDBSqlite(os.path.join(PROJ_DIR, 'Django', 'PG', 'db.sqlite3'))
    self.__db = CDBPostgresql('tools', 'king', 'wqlwqlwql', '108.61.200.192')
    self.__compress = CCompress()
    self.__rMin = self.Settings['Min']

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
    self.__Web.ExecScript("javascript:__doPostBack('ctl00$CP1$gvProblems','Sort$Text2')")
    #self.__Web.WaitUntil('visibility_of_element_located', self.Settings['Buttons']['SortIconAsc']['By'], self.Settings['Buttons']['SortIconAsc']['Arg'])
    self.__ss.Sleep(2)
    # self.__Web.WaitUntil('text_to_be_present_in_element', self.__selfSettings['Buttons']['Sort']['By'], self.__selfSettings['Buttons']['Sort']['Arg'], ' ')
    self.__Web.ExecScript("javascript:__doPostBack('ctl00$CP1$gvProblems','Sort$Text2')")
    # if self.Settings['Driver']['use'] == 2:
    #self.__Web.WaitUntil('visibility_of_element_located', self.Settings['Buttons']['SortIconDesc']['By'], self.Settings['Buttons']['SortIconDesc']['Arg'])
    self.__ss.Sleep(2)
    # else:
    #   self.__ss.Sleep(1)
    #   self.__Web.WaitUntil('invisibility_of_element_located', self.__selfSettings['Buttons']['WaitingPanel']['By'], self.__selfSettings['Buttons']['WaitingPanel']['Arg'])

  def __RegRevisions(self, src):
    src = re.sub(re.compile(r'&nbsp;'), '', src)
    pattern1 = re.compile(self.Settings['RegExp']['Revisions']['Re'], re.S)
    items = re.findall(pattern1, src)
    pattern2 = re.compile(r',|，')
    b = False
    self.__db.cursor.execute('select max(id) from XXSY_URTracker;')
    idx = self.__db.cursor.fetchone()[0] or 0
    for item in items:
      # if idx > 10:
      #   break
      if item[4] == '' or item[4] == ' ' or item[4] == u'\xa0':
        continue
      revisions_s = re.split(pattern2, item[4])
      for r in revisions_s:
        if self.__CfgFilePath == 'XXSY.json':
            if int(r) >= self.__rMin:
              idx += 1
              # print str(idx), item[0], item[1], item[2], str(r), item[4]
              print idx, item[0], item[1].encode('utf-8'), item[2].encode('utf-8'), str(r), item[6], str(self.Settings['URTracker']['Project'])
              self.__db.cursor.execute('insert into XXSY_URTracker (id, url, title, state, revision, task, project) values (%s, %s, %s, %s, %s, %s, %s);', (idx, item[0], item[1].encode('utf-8'), item[2].encode('utf-8'), str(r), item[6], str(self.Settings['URTracker']['Project'])))

      if item[2] in self.Settings['RegExp']['Revisions']['States_NotEnd']: 
        b = True

    return b

  def GetRevisions(self):
    self.__db.cursor.execute('delete from XXSY_URTracker where project = 0 or project =' + str(self.Settings['URTracker']['Project']))
    HTMLs = []
    HTMLs.append(self.__Web.GetPageSource())
    pageIdx = 2
    numIdx = 2
    while pageIdx <= self.__PageNum:
      self.__Web.ExecScript('javascript:__doPostBack(\'ctl00$CP1$gvProblems\',\'Page$' + str(pageIdx) + '\')')
      if numIdx > 10:
        numIdx = 8
      if not self.__RegRevisions(HTMLs[pageIdx - 2]):
        break
      time.sleep(3)
      # self.__Web.WaitUntil('visibility_of_element_located', self.__selfSettings['Buttons']['NumberSelected']['By'], self.__selfSettings['Buttons']['NumberSelected']['Arg'][0] + str(pageIdx) + self.__selfSettings['Buttons']['NumberSelected']['Arg'][1])
      HTMLs.append(self.__Web.GetPageSource())
      pageIdx += 1
      numIdx += 1

    self.__RegRevisions(HTMLs[pageIdx - 2])

    self.__db.Commit()
    self.__db.Close()
    self.__Web.Quit()

  def URTrackerCheck(self, args):
    try:
      self.__Login()
      self.__GoToBranchPage(args['URTracker_Branch'])
      self.__PageNum = self.__GetBranchPageNum()
      self.__SortPage()
      self.GetRevisions()
    except Exception, e:
      self.__db.Commit()
      self.__db.Close()
      self.__Web.Quit()
      self.__ss.Traceback(Exception, e)      

class CPGSVN:
  def __init__(self, CfgFilePath):
    # 降低耦合，多取一次文件吧
    self.Settings = CSettings(CfgFilePath).Json()
    self.__svnPath = self.Settings['SVNPath']['Branch']
    self.__rMin = self.Settings['Min']
    self.__ss = CSystem()
    self.__logs = ''
    self.__logItems = {}
    # self.__db = CDBSqlite(os.path.join(PROJ_DIR, 'Django', 'PG', 'db.sqlite3'))
    print 1
    self.__db = CDBPostgresql('tools', 'king', 'wqlwqlwql', '108.61.200.192')
    print 2
    self.__cursor = self.__db.cursor
    self.__GetLogs()

  def __GetLogs(self):
    self.__logs = self.__ss.RunProcess(u'svn log -r ' + str(self.__rMin) + ':' + 'HEAD' + ' ' + self.__svnPath, True)
    pattern = re.compile(self.Settings['RegExp']['SVN']['Re'], re.S)
    items = re.findall(pattern, self.__logs)
    try:
      self.__cursor.execute('select max(revision) from XXSY_SVNLog')
      __max = self.__cursor.fetchone()[0]
    except:
      pass
    __max = __max if __max else self.__rMin

    for item in items:
      if int(item[0]) < int(__max) and __max != self.__rMin:
        continue
      # print item[0]
      self.__db.cursor.execute('select 1 from XXSY_SVNLog where revision=' + str(item[0]))
      try:
        self.__cursor.fetchone()[0]
      except:
      # if not self.__db.cursor.fetchone():
        if self.__ss.GetSystemFlag() != 'Linux':
          print(item[0])
          self.__db.cursor.execute('insert into XXSY_SVNLog (revision, author, svnDate, log) values (%s, %s, %s, %s)', (str(item[0]), str(item[1]), str(item[2]), str(item[3]).decode('gbk') if item[3] else ''))
        else:
          # print item[3]
          self.__db.cursor.execute('insert into XXSY_SVNLog (revision, author, svnDate, log) values (%s, %s, %s, %s)', (str(item[0]), str(item[1]), str(item[2]), str(item[3]) if item[3] else ''))
    self.__db.Commit()
    self.__db.Close()

class CPGDB:
  def __init__(self, txtFile):
    self.__ss = CSystem()
    self.__txtFile = self.__ss.ReadFile(os.path.join(PROJ_DIR, 'DBs', 'PG', txtFile))
    self.__db = CDBPostgresql('tools', 'king', 'wqlwqlwql', '108.61.200.192')
    # print self.__txtFile

  def Convert(self):
    pass
