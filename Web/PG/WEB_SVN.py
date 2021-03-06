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
        if ss.IsProcessRunning(cfg['Cookie']):
                return
	cfg['Driver']['use'] = 1 if ss.GetSystemFlag() == 'Linux' else cfg['Driver']['use']

	web = CPG_WEB(self.CfgFilePath)
	web.URTrackerCheck({
  		'URTracker_Branch' : cfg['URTracker']['Branch'] + str(cfg['URTracker']['Project']),
  		})

	svn = CPG_SVN(self.CfgFilePath)

        db = CDBPostgresql('tools', 'king', 'wqlwqlwql', '108.61.200.192')
        db.cursor.execute('update xxsy_misc set value = (select now() + \'8 h\') where id = 1;')
        db.Commit()
        db.Close()

	if ss.GetSystemFlag() == 'Linux':
		ss.KillProcess([cfg['Cookie']], [cfg['Cookie']])
	else:
		ss.KillProcess([cfg['Driver'][cfg['Driver']['use']] + '*'])
