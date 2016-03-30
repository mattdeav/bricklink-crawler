import re
from setitem import *
from bs4 import BeautifulSoup
import urllib2
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class category(object):
    def __init__(self, catname, caturl):
        self.catname = catname.strip()
        self.caturl = caturl
        self.pages = []
        self.pages.append(caturl)
        self.sets = []
        self.html = self.htmlclean(self.openurl(self.caturl))
        
        # f = open('F:/sets/testcat.txt','w')

        
        self.findnextpages()
        for item in self.sets:
            newset = setitem(item, self.catname)
        
        # DO WE NEED THIS?
        #self.findsets()
        
    def htmlclean(self, url):
        soup = BeautifulSoup(url.read())
        temp = ' '.join(soup.prettify().encode('UTF-8').split())
        temp = temp.replace('&amp;','&')
        return temp
    
    def openurl(self, new):
        if "bricklink" in new:
            return urllib2.urlopen(new)
        else:
            return urllib2.urlopen("http://www.bricklink.com" + new)

    def findsetlinks(self):
        for pg in self.pages:
            print "PAGE", pg
            catpage = self.openurl(pg)
            catpage = self.htmlclean(catpage)
            
            response = HtmlResponse(url="http://www.bricklink.com" + pg, body=catpage)
            selector = Selector(response=response)
            
            for set in selector.xpath('//a[contains(@href, "catalogItem.")]/@href'):
                if not set.extract().replace('&amp;','&') in self.sets:
                    self.sets.append(set.extract().replace('&amp;','&'))
            
            # csv = re.findall(r'Set No: ([\S]*) Name: ([^"]*).*?Parts.*?, ([0-9]{4}).*?href="/browseList.asp\?itemType=\w&catString=[0-9]+.[0-9]+">(\D*)</a.*?href="(/catalogItem[^"]*)">', html)

            # for item in csv:
                # print item[0],item[1],item[2],item[3],item[4]
                # self.setsarray.append(setitem(item[0],item[1],item[2],item[3],item[4]))

    def findnextpages(self):
        response = HtmlResponse(url=self.caturl, body=self.html)
        selector = Selector(response=response)

        for pglink in selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table/tr[3]/td'):
            for link in pglink.xpath('.//a'):
                if "pg=" in link.extract() and not "> Next <" in link.extract():
                    lnk = re.findall(r'href="([a-zA-Z/\.\?0-9=&;]*)', link.extract())
                    if lnk[0].replace('&amp;','&') not in self.pages:
                        self.pages.append(lnk[0].replace('&amp;','&'))
                        
        self.findsetlinks()
        
    def findsets(self):
        f = open("F:/sets/sets.txt", 'a')
        towrite = True
        for itemset in self.sets:
            for line in open('F:/sets/sets.txt', 'r'):
                if itemset in line:
                    towrite = False
                    break
            if towrite:
                f.write(itemset + "\n")
            else:
                towrite = True
        f.close()
        
    def __str__(self):
        return self.catname + ", " + self.caturl