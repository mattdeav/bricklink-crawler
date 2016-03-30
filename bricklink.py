# This file is step 1

from bs4 import BeautifulSoup
import urllib2
import os
import re
from setitem import *
from category import *
import time
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


def htmlclean(url):
    soup = BeautifulSoup(url.read())
    temp = ' '.join(soup.prettify().encode('UTF-8').split())
    temp = temp.replace('&amp;','&')
    return temp

def openurl(new):
    if "bricklink" in new:
        return urllib2.urlopen(new)
    else:
        return urllib2.urlopen("http://www.bricklink.com" + new)

dirpath = "F:/sets/"

categoriespage = 'http://www.bricklink.com/catalogTree.asp?itemType=S'
categorieshtml = urllib2.urlopen('http://www.bricklink.com/catalogTree.asp?itemType=S')
categorieshtml = htmlclean(categorieshtml)

response = HtmlResponse(url=categoriespage, body=categorieshtml)
selector = Selector(response=response)

# Keeping categories in case of log save after
categories = []
categories_list = re.findall(r'href="([^\"]*catString=[0-9]*)">(\D*)<', categorieshtml)

    
lastcategory = ''
second_to_last = ''

try:
    file = open('F:/sets/sets.txt','r')
    for line in open('F:/sets/sets.txt','r'):
        fields = line.split('|')
        if lastcategory != fields[3]:
            second_to_last = lastcategory
            lastcategory = fields[3]
            
        if not lastcategory in categories:
            categories.append(lastcategory)
except:
    file = open('F:/sets/sets.txt','w')
    file.close()

if not lastcategory == '':
    started = False
else:
    started = True
for catlink in categories_list:
    if catlink[1].strip() == lastcategory:
        started = True
        print('last cat: ' + catlink[1].strip())
    if started:
        print('Running: ' + catlink[1].strip())
        categories.append(category(catlink[1].strip(), "http://www.bricklink.com" + catlink[0].strip()))

    
    
    
    
    
    