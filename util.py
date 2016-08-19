#coding: utf-8
import os
import re
import time
import platform
import subprocess

class settings:
    def __init__(self):
        self.projectPath = ''
        self.serverFilesPath = 'D:\\XMZ\\bo2_svr\\svr\\'
        self.serverToosPath = 'D:\\XMZ\\bo2_svr\\tools\\'
        self.mySQL = 'mysql -h192.168.6.55 -uroot -ppixeldb2015 -Dxmz_homeKing < '

    def getPath(self, name):
        if name == 'project':
            return self.projectPath
        elif name == 'server':
            return self.serverFilesPath
        elif name == 'serverTools':
            return self.serverToosPath

    def getMySQLCMD(self):
        return self.mySQL

class util:
    def __init__(self):
        pass

    def systemFlag(self):
        return platform.system()

    def walkPath(self, path):
        if path == '':
            print 'Error path'
            return
        # dirPath, dirNames, fileNames
        return os.walk(path)

    def getTime(self, cm, filePath):
        if cm == 'c':
            return os.path.getctime(filePath)
        elif cm == 'm':
            return os.path.getmtime(filePath)

    def writeFile(self, filePath, blocks):
        file = open(filePath, 'w+')
        file.write(blocks)
        file.close()

    def readFile(self, filePath):
        file = open(filePath, 'r+')
        text = file.read()
        file.close()
        return text

    def killProcess(self, names):
        if not isinstance(names, list):
            print 'Arg 2 must be a list'
            return
        for name in names:
            print name
            os.system('start taskkill /f /im ' + name)

    def runProcess(self, path, usepopen = False):
        if usepopen:
            return os.popen(path).read()
        return subprocess.call(path, shell = False)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class WebElement:
    def __init__(self, driver):
        self.driver = driver    
        self.element = 0
    def find(self, enum, arg):
        enum = enum.lower()
        try:
            if enum == 'name':
                self.element = self.driver.find_element_by_name(arg)
            elif enum == 'xpath':
                self.element = self.driver.find_element_by_xpath(arg)
            elif enum == 'id':
                self.element = self.driver.find_element_by_id(arg)
            elif enum == 'tagname':
                self.element = self.driver.find_element_by_tag_name(arg)
        except:
            self.driver.Quit()
    def sendKeys(self, s):
        self.element.send_keys(s)

class Web:
    CU = util()
    def __init__(self):
        sysstr = platform.system()
        if sysstr == 'Linux':
            self.__class__.CU.runProcess('chmod +x ./phantomjs', usepopen = True)
            # self.driver = webdriver.PhantomJS(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'phantomjs'))
            self.driver = webdriver.Chrome()
        elif sysstr == 'Windows':
            self.driver = webdriver.PhantomJS('./phantomjs_win.exe')
            # self.driver = webdriver.Chrome()
        elif sysstr == 'Darwin':
            # self.__class__.CU.runProcess('chmod +x ./phantomjs', usepopen = True)
            # self.driver = webdriver.PhantomJS(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'phantomjs'))
            self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)

    def Goto(self, page):
        page = page.lower()
        if not re.match(r'http', page):
            page = 'http://' + page
        self.driver.get(page)

    def GoBack(self):
        self.driver.back()
    def Forward(self):
        self.driver.forward()

    def GetPageSource(self):
        return self.driver.page_source

    def WaitUntil(self, condition, enum, arg):
        enum = enum.lower()
        if condition == 'invisibility_of_element_located':
            cmd = EC.invisibility_of_element_located
            if enum == 'xpath':
                self.wait.until(cmd(By.XPATH, arg))
        elif condition == 'element_to_be_clickable':
            cmd = EC.element_to_be_clickable
            if enum == 'xpath':
                self.wait.until(cmd(By.XPATH, arg))

    def ExecScript(self, script):
        self.driver.execute_script(script)

    def Quit(self):
        self.driver.quit()
