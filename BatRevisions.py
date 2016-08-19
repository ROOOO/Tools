#coding: utf-8

from util import *
from selenium.webdriver.common.keys import Keys

class BR:
    def __init__(self):
        self.util = util()
        self.web = Web()
        self.element = WebElement(self.web.driver)
        self.loginURL = 'http://192.168.5.143/urtracker/Pts/home.aspx'
        self.loginU = 'wangqinlei'
        self.loginP = 'djCy!3Skc&bNPvqQ9WnxGd6Io8bEvhlJ'
        self.tHtmls = []
        self.tPages = 0
        self.tURLs = []

    def Login(self):
        self.web.Goto(self.loginURL)
        self.element.find('name', 'txtEmail').sendKeys(self.loginU)
        self.element.find('name', 'txtPassword').sendKeys(self.loginP).sendKeys(Keys.RETURN)
        self.web.WaitUntil('invisibility_of_element_located', 'xpath', '//div//table//td//a[@onclick="TreeView_SelectNode(ctl00_CP1_tvNav_Data, this,\'ctl00_CP1_tvNavt14\');"]')

    def GetPages(self):
        self.tPages = 0

    def GetHTMLs(self):
        self.tHtmls = []

    def GetURLs(self):
        self.tURLs = []

    def GetMessages(self):
        self.GetPages()
        self.GetHTMLs()
        self.GetURLs()

    def SwitchURLs(self):
        pass

    def PostProcessGetMessages(self):
        self.SwitchURLs()

    def ProcessSubmit(self):
        pass

    def ProcessURLs(self):
        for url in self.tURLs:
            self.ProcessSubmit()

    def Run(self):
        self.Login()
        self.GetMessages()
        self.PostProcessGetMessages()
        self.ProcessURLs()
        
if __name__ == '__main__':
    b = BR()
    b.Run()
