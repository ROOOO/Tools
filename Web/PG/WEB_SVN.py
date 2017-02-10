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
	db = CDBSqlite(os.path.join(PROJ_DIR, 'Django', 'PG', 'db.sqlite3'))
	cfg['Driver']['use'] = 1 if ss.GetSystemFlag() == 'Linux' else cfg['Driver']['use']

	web = CPG_WEB(self.CfgFilePath)
	web.URTrackerCheck({
  		'URTracker_Branch' : cfg['URTracker']['Branch'],
  		})

	_min = db.cursor.execute('select min(revision) from XXSY_URTracker where state != "交付完成" order by revision;').fetchone()[0]
	_max = db.cursor.execute('select max(revision) from XXSY_URTracker where state != "交付完成" order by revision;').fetchone()[0]
	svn = CPG_SVN(self.CfgFilePath)

	if ss.GetSystemFlag() == 'Linux':
		ss.KillProcess([cfg['Cookie']], [cfg['Cookie']])
	else:
		ss.KillProcess([cfg['Driver'][cfg['Driver']['use']] + '*'])
