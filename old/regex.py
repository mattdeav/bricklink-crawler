# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import urllib2
import os
import re


def htmlclean():
    
    soup = BeautifulSoup(urllib2.urlopen('http://www.bricklink.com/catalogPG.asp?S=70400-1').read())
    temp = ' '.join(soup.prettify().encode('UTF-8').split())
    temp = temp.replace('&amp;','&')
    return temp

text = htmlclean()
csv = re.findall(r'Times Sold.*?b> ([0-9]*).*?Total Qty.*?b> ([0-9]*).*?Min Price.*?b> US...([0-9.]*).*?Avg Price.*?b> US...([0-9.]*).*?Max Price.*?b> US...([0-9.]*)',text)

if len(csv)>1:
    numsets = int(csv[0][1])
    
    for i in range(1,len(csv)):
        numsets = numsets - int(csv[i][1])
    
    newprice = csv[0]
    if not numsets == 0:
        usedprice = csv[1]

current = re.findall(r'Total Lots.*?b> ([0-9]*).*?Total Qty.*?b> ([0-9]*).*?Min Price.*?b> US...([0-9.]*).*?Avg Price.*?b> US...([0-9.]*).*?Max Price.*?b> US...([0-9.]*)',text)

currentnewprice = current[0]
if not len(current) == 1:
    currentusedprice = current[1]