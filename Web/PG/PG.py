#coding: utf-8

import sys
sys.path.append('../..')
from util.util import *
sys.path.pop(len(sys.path) - 1)

class CPG:
  def __init__(self, CfgFilePath):
    cfg = CSettings(CfgFilePath)
    self.Settings = cfg.Json()
    self.Web = CWeb(self.Settings)

  def __Login__(self, html = 'http://192.168.5.143/urtracker/Pts/home.aspx'):
    pass

  def __GetHTML(self):
    pass

  def GetRevisions(self):
    pass

  def URTrackerCheck(self, reg):
    self.__Login()
    self.__GetHTML()
    self.GetRevisions(reg)

