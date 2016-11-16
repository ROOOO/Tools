#coding: utf-8

from PG import *

class CXMZ_WEB(CPGTracker):
  def __init__(self, CfgFilePath):
    CPGTracker.__init__(self, CfgFilePath)

class CXMZ_SVN(CPGSVN):
  def __init__(self, CfgFilePath, rMin, rMax):
    CPGSVN.__init__(self, CfgFilePath, rMin, rMax)

if __name__ == '__main__':
	xmz_cfg = CSettings('XMZ.json').Json()
	xmz_ss = CSystem()
	xmz_cfg['Driver']['use'] = 1 if xmz_ss.GetSystemFlag() == 'Linux' else xmz_cfg['Driver']['use']

	xmz_web = CXMZ_WEB('XMZ.json')
	revisions = xmz_web.URTrackerCheck({
  		'URTracker_Branch' : xmz_cfg['URTracker']['Branch'],
  		})

	_min = revisions[3]
	_max = revisions[4]
	xmz_svn = CXMZ_SVN('XMZ.json', _min if _min < xmz_cfg['Min'] and _min != 0 else xmz_cfg['Min'], _max)
	lists = xmz_svn.CheckLogs(list(revisions[0]) + list(revisions[1]), revisions[2])
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
		if int(w) >= int(xmz_cfg['Min']):
			print w
			block += str(w) + '\t' + on_and_off_d[str(w)].url + '\t' + 'wrong\n'

	TMP_FILE = os.path.join(xmz_ss.GetDirName(xmz_ss.GetDirName(xmz_ss.GetRealPath(__file__))), 'PG_OUTPUTS', '_xmz_tracker_svn.txt')
	FILE = os.path.join(xmz_ss.GetDirName(xmz_ss.GetDirName(xmz_ss.GetRealPath(__file__))), 'PG_OUTPUTS', 'xmz_tracker_svn.txt')

	block += ','.join(revisions[2])
	block += ',\n'

	xmz_ss.WriteFile(TMP_FILE, block)
	xmz_ss.CopyFile(TMP_FILE, FILE)

	# xmz_ss.RunProcess('scp "' + FILE + '" wangqinlei@192.168.6.55:/home/wangqinlei/PGTools/checkResult_xmz.txt', True)

	if xmz_ss.GetSystemFlag() == 'Linux':
		xmz_ss.KillProcess([xmz_cfg['Cookie']], [xmz_cfg['Cookie']])
	else:
		xmz_ss.KillProcess([xmz_cfg['Driver'][xmz_cfg['Driver']['use']] + '*'])
