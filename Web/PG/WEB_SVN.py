#coding: utf-8

from PG import *

class CXXSY_WEB(CPGTracker):
  def __init__(self, CfgFilePath):
    CPGTracker.__init__(self, CfgFilePath)

class CXXSY_SVN(CPGSVN):
  def __init__(self, CfgFilePath, rMin, rMax):
    CPGSVN.__init__(self, CfgFilePath, rMin, rMax)

class CWEB_SVN:
  def __init__(self, CfgFilePath, ProjName):
  	self.CfgFilePath = CfgFilePath
  	self.ProjName = ProjName
  def Run(self):
	cfg = CSettings(self.CfgFilePath).Json()
	ss = CSystem()
	cfg['Driver']['use'] = 1 if ss.GetSystemFlag() == 'Linux' else cfg['Driver']['use']

	web = CXXSY_WEB(self.CfgFilePath)
	revisions = web.URTrackerCheck({
  		'URTracker_Branch' : cfg['URTracker']['Branch'],
  		})

	_min = revisions[4][0]
	_max = revisions[5][0]
	svn = CXXSY_SVN(self.CfgFilePath, _min if _min < cfg['Min'] and _min != 0 else cfg['Min'], _max)
	lists = svn.CheckLogs(list(revisions[0]) + list(revisions[1]), revisions[2])
	blackList = lists[0]
	blackList.sort()
	wrongList = lists[1]
	wrongList.sort()

	revisions[2].sort()

	block = ''
	for t in revisions[3]:
		# print t, revisions[3][t]
		block += t + '\t' + revisions[3][t] + '\t' + 'testing\n'

	for b in blackList:
		print b.revision, b.author, b.time, b.log
		logs = b.log.decode('gb2312').encode('utf-8')
		block += 'black\t' + b.revision + '\t' + b.author + '\t' + b.time + '\t"""' + logs + '"""\t' + 'black\n'
		# block += b.revision + '\t' + b.author + '\t' + b.time + '\t' + 'black\n'

	on_and_off_d = revisions[0].copy()
	on_and_off_d.update(revisions[1])

	print '\nWRONG LIST:'
	for w in wrongList:
		if int(w) >= int(cfg['Min']):
			print w
			block += str(w) + '\t' + on_and_off_d[str(w)].url + '\t' + 'wrong\n'

	TMP_FILE = os.path.join(ss.GetDirName(ss.GetDirName(ss.GetRealPath(__file__))), 'PG_OUTPUTS', '_' + self.ProjName + 'tracker_svn.txt')
	FILE = os.path.join(ss.GetDirName(ss.GetDirName(ss.GetRealPath(__file__))), 'PG_OUTPUTS', self.ProjName + 'tracker_svn.txt')

	block += ','.join(revisions[2])
	block += ',\n'

	ss.WriteFile(TMP_FILE, block)
	ss.CopyFile(TMP_FILE, FILE)

	# ss.RunProcess('scp "' + FILE + '" wangqinlei@192.168.6.55:/home/wangqinlei/PGTools/checkResult_xxsy.txt', True)

	if ss.GetSystemFlag() == 'Linux':
		ss.KillProcess([cfg['Cookie']], [cfg['Cookie']])
	else:
		ss.KillProcess([cfg['Driver'][cfg['Driver']['use']] + '*'])
