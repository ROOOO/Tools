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

	_min = revisions[3]
	_max = revisions[4]
	xxsy_svn = CXXSY_SVN('XXSY.json', _min if _min < xxsy_cfg['Min'] and _min != 0 else xxsy_cfg['Min'], _max)
	lists = xxsy_svn.CheckLogs(list(revisions[0]) + list(revisions[1]), revisions[2])
	blackList = lists[0]
	blackList.sort()
	wrongList = lists[1]
	wrongList.sort()

	revisions[2].sort()

	block = ''
	for b in blackList:
		print b.revision, b.author, b.time, b.log
		# block += b.revision + '\t' + b.author + '\t' + b.time + '\t"' + b.log + '"\t' + 'eol\n'
		block += b.revision + '\t' + b.author + '\t' + b.time + '\t' + 'black\n'

	on_and_off_d = revisions[0].copy()
	on_and_off_d.update(revisions[1])

	print '\nWRONG LIST:'
	for w in wrongList:
		if int(w) >= int(xxsy_cfg['Min']):
			print w
			block += str(w) + '\t' + on_and_off_d[str(w)].url + '\t' + 'wrong\n'

	TMP_FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))), 'PG_OUTPUTS', '_xxsy_tracker_svn.txt')
	FILE = os.path.join(xxsy_ss.GetDirName(xxsy_ss.GetDirName(xxsy_ss.GetRealPath(__file__))), 'PG_OUTPUTS', 'xxsy_tracker_svn.txt')

	block += ','.join(revisions[2])
	block += ',\n'

	xxsy_ss.WriteFile(TMP_FILE, block)
	xxsy_ss.CopyFile(TMP_FILE, FILE)

	# xxsy_ss.RunProcess('scp "' + FILE + '" wangqinlei@192.168.6.55:/home/wangqinlei/PGTools/checkResult_xxsy.txt', True)

	if xxsy_ss.GetSystemFlag() == 'Linux':
		xxsy_ss.KillProcess([xxsy_cfg['Cookie']], [xxsy_cfg['Cookie']])
	else:
		xxsy_ss.KillProcess([xxsy_cfg['Driver'][xxsy_cfg['Driver']['use']] + '*'])
