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
	xxsy_ss = CSystem()
	xxsy_cfg['Driver']['use'] = 1 if xxsy_ss.GetSystemFlag() == 'Linux' else xxsy_cfg['Driver']['use']

	xxsy_web = CXXSY_WEB('XXSY.json')
	revisions = xxsy_web.URTrackerCheck({
  		'URTracker_Branch' : xxsy_cfg['URTracker']['Branch'],
  		})

	_min = min(revisions[0]) if min(revisions[0]) < min(revisions[1]) else min(revisions[1])
	_max = max(revisions[0]) if max(revisions[0]) < max(revisions[1]) else max(revisions[1])
	xxsy_svn = CXXSY_SVN('XXSY.json', _min if _min < xxsy_cfg['Min'] else xxsy_cfg['Min'], _max)
	lists = xxsy_svn.CheckLogs(revisions[0] + revisions[1], revisions[2])
	blackList = lists[0]
	blackList.sort()
	wrongList = lists[1]
	revisions[2].sort()

	block = ''
	for b in blackList:
		print b.revision, b.author, b.time, b.log
		# block += b.revision + '\t' + b.author + '\t' + b.time + '\t"' + b.log + '"\t' + 'eol\n'
		block += b.revision + '\t' + b.author + '\t' + b.time + '\t' + 'black\n'
	print 'WRONG LIST:\n'
	for w in wrongList:
		print w
		block += str(w) + 'wrong\n'

	TMP_FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))), 'PG_OUTPUTS', '_xxsy_tracker_svn.txt')
	FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))), 'PG_OUTPUTS', 'xxsy_tracker_svn.txt')

	# todo
	block += ','.join(revisions[2])
	block += ',\n'
	block += xxsy_ss.StrfTime(xxsy_ss.GetFileTime('m', TMP_FILE)) + '\n'

	xxsy_ss.WriteFile(TMP_FILE, block)
	xxsy_ss.CopyFile(TMP_FILE, FILE)

	xxsy_ss.RunProcess('scp "' + FILE + '" wangqinlei@192.168.6.55:/home/wangqinlei/PGTools/checkResult_xxsy.txt', True)

	if xxsy_ss.GetSystemFlag() == 'Linux':
		xxsy_ss.KillProcess([xxsy_cfg['Cookie']], [xxsy_cfg['Cookie']])
	else:
		xxsy_ss.KillProcess([xxsy_cfg['Driver'][xxsy_cfg['Driver']['use']] + '*'])
