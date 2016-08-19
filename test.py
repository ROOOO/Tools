from util import *
w1 = Web()
w1.Goto('www.baidu.com')
# w1.GoBack()

e1 = WebElement(w1)
e1.find('name', 'wd').sendKeys('123')

w1.Quit()
