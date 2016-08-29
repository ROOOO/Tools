#coding: utf-8
from util import *
import thread
w1 = Web()
def switchToAlert():
    w1.WaitUntil('alert_is_present')
    w1.driver.switch_to_alert().accept()
    print '---'
print '==='
thread.start_new_thread(switchToAlert, ())
# w1.ExecScript('confirm("H")')
print '==='
try:
    a = w1.driver.switch_to_alert()
except:
    print 'aa'
else:
    a.accept()
# w1.Goto('http://192.168.5.143/urtracker/Pts/home.aspx')
# w1.GoBack()

# e1 = WebElement(w1.driver)
# e = e1.find('name', 'wd').sendKeys('123')

# u = util()
# u.sleep(3)

w1.Quit()
