#coding: utf-8

from PG import *

class CXXSY_WEB(CPGTracker):
  def __init__(self, CfgFilePath):
    CPGTracker.__init__(self, CfgFilePath)

class CXXSY_SVN(CPGSVN):
  def __init__(self, CfgFilePath, rMin, rMax):
    CPGSVN.__init__(self, CfgFilePath, rMin, rMax)

if __name__ == '__main__':
	xxsy_cfg = CSettings('XXSY.json').Json()

	xxsy_web = CXXSY_WEB('XXSY.json')
	revisions = xxsy_web.URTrackerCheck({
  		'URTracker_Branch' : xxsy_web.Settings['URTracker']['Branch'],
  		})

	_min = min(revisions[0]) if min(revisions[0]) < min(revisions[1]) else min(revisions[1])
	_max = max(revisions[0]) if max(revisions[0]) < max(revisions[1]) else max(revisions[1])
	xxsy_svn = CXXSY_SVN('XXSY.json', _min if _min < xxsy_cfg['Min'] else xxsy_cfg['Min'], _max)
	blackList = xxsy_svn.CheckLogs(revisions[0] + revisions[1])
	for b in blackList:
		print b.revision, b.author, b.time, b.log
