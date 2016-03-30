import re
from priceguide import *
from bs4 import BeautifulSoup
import urllib2
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class part(object):
    def __init__(self, partnum, partname, partcolor, parttype, parturl):
        self.partname = partname
        self.partnum = partnum
        self.partcolor = partcolor
        self.parturl = parturl
    
    def __str__(self):
        return (self.category.strip() + ", " + self.setnum + ", " + self.setname + ", " + self.year + ", " + str(self.weight) + ", " + self.catalogpage)
     

    def htmlclean(self, url):
        soup = BeautifulSoup(url.read())
        temp = ' '.join(soup.prettify().encode('utf-8').split())
        temp = temp.replace('&amp;','&')
        return temp
        
    def openurl(self, new):
        return urllib2.urlopen("http://www.bricklink.com" + new)
        
    