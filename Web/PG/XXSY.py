#coding: utf-8

from PG import CPG

class CXXSY(CPG):
  def __init__(self, CfgFilePath):
    CPG.__init__(self, CfgFilePath)
    self.SVNPath = self.Settings['SVNPath']['branch']

  def URTrackerCheck(self):
    pass

  def Login(self):
  	CPG.__Login__(self)

if __name__ == '__main__':
	xxsy = CXXSY('XXSY.json')
	print xxsy.SVNPath
	xxsy.Login()
