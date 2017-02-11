#coding: utf-8

from PG import *
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CPG_WEB(CPGTracker):
  def __init__(self, CfgFilePath):
    CPGTracker.__init__(self, CfgFilePath)

class CPG_SVN(CPGSVN):
  def __init__(self, CfgFilePath):
	CPGSVN.__init__(self, CfgFilePath)

class CWEB_SVN:
  def __init__(self, CfgFilePath, ProjName):
  	self.CfgFilePath = CfgFilePath
  	self.ProjName = ProjName
  def Run(self):
	cfg = CSettings(self.CfgFilePath).Json()
	ss = CSystem()
	cfg['Driver']['use'] = 1 if ss.GetSystemFlag() == 'Linux' else cfg['Driver']['use']

	web = CPG_WEB(self.CfgFilePath)
	web.URTrackerCheck({
  		'URTracker_Branch' : cfg['URTracker']['Branch'],
  		})

	svn = CPG_SVN(self.CfgFilePath)

	if ss.GetSystemFlag() == 'Linux':
		ss.KillProcess([cfg['Cookie']], [cfg['Cookie']])
	else:
		ss.KillProcess([cfg['Driver'][cfg['Driver']['use']] + '*'])
