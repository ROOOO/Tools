#coding: utf-8
from util import *
w1 = Web()
w1.Goto('http://192.168.5.143/urtracker/Pts/home.aspx')
# w1.GoBack()

e1 = WebElement(w1.driver)
e = e1.find('name', 'wd').sendKeys('123')

u = util()
u.sleep(3)

w1.Quit()
