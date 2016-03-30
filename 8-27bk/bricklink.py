from bs4 import BeautifulSoup
import urllib2
import os
import re
from setitem import *
from category import *
import time
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

def findcategories(html):
    csv = re.findall(r'href="([^\"]*catString=[0-9]*)">(\D*)<', html)
    categories = []
    
    for cat in csv:
        categories.append(category(cat[1].strip(), "http://www.bricklink.com" + cat[0].strip()))
        
    return categories

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

categoriespage = 'http://www.bricklink.com/browseTree.asp?itemType=S'
categorieshtml = urllib2.urlopen('http://www.bricklink.com/browseTree.asp?itemType=S')
categorieshtml = htmlclean(categorieshtml)

response = HtmlResponse(url=categoriespage, body=categorieshtml)
selector = Selector(response=response)
categories = []

# singlecat = category("STARWARS","http://www.bricklink.com/browseList.asp?itemType=S&catString=9")
# singleset = setitem("/catalogItem.asp?S=10167-1","na")

lastcategory = ''
categories = []
# try:
    # for line in open('F:/sets/sets.txt','r'):
        # fields = line.split('|')
        # lastcategory = fields[3]
        # if not lastcategory in categories:
            # categories.append(lastcategory)
            # print lastcategory
        # #break
# except IOError:
    # lastcategory = ''
categories = findcategories(categorieshtml)
    
print "print categories"
for cat in categories:
    print cat
    
print "end categories"

for catlink in selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table/tr[4]'):
    for cat in catlink.xpath('.//b/a'):
        catregex = re.findall(r'href="([a-zA-Z/\.\?0-9=&;]*)', cat.extract())
        catname = re.findall(r'>([\(\)a-zA-Z0-9 \-\.&;\:\/\'\{\}]*)<',cat.extract())
        for categ in catregex:
            if not catname[0].strip() in categories or catname[0].strip() == lastcategory:
                print "LC", catname[0], lastcategory
                newcategory = category(catname[0],categ.encode('utf-8').replace('&amp;','&'))
                #categories.append(newcategory)

    
    
    
    
    
    