import re
import urllib2
from setitem import *
from bs4 import BeautifulSoup
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
        
        self.findnextpages(caturl.split('&')[1])
        x = 0
        for item in self.sets:
            print(item)
        for item in self.sets:
            if not '?O=' in item and not '?I=' in item:
                item = 'http://alpha.bricklink.com/pages/clone/' + item.replace('http://alpha.bricklink.com/pages/clone/','')
                x = x + 1
                # print('from category ' + item)
                print("Running set # " + str(x) + " of " + str(len(self.sets)) + ". Set name: " + item)
                newset = setitem(item, self.catname)
                # break to only do one set
                # break
            
        
        # DO WE NEED THIS?
        # I think this is to re-run if last time failed
        # self.findsets()
        
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
            catpage = self.openurl(pg)
            catpage = self.htmlclean(catpage)
            
            response = HtmlResponse(url="http://www.bricklink.com" + pg, body=catpage)
            selector = Selector(response=response)
            
            for set in selector.xpath('//a[contains(@href, "catalogitem.")]/@href'):
                setlink = set.extract().replace('&amp;','&')
                if not setlink in self.sets:
                    self.sets.append(setlink)
            
            # csv = re.findall(r'Set No: ([\S]*) Name: ([^"]*).*?Parts.*?, ([0-9]{4}).*?href="/browseList.asp\?itemType=\w&catString=[0-9]+.[0-9]+">(\D*)</a.*?href="(/catalogItem[^"]*)">', html)

            # for item in csv:
                # print item[0],item[1],item[2],item[3],item[4]
                # self.setsarray.append(setitem(item[0],item[1],item[2],item[3],item[4]))

    def findnextpages(self, catstringurl):
        response = HtmlResponse(url=self.caturl, body=self.html)
        selector = Selector(response=response)
        
        for pglink in selector.xpath('//a[contains(@href, "' + catstringurl + '")]/@href'):
            page = (pglink.extract().encode('utf-8'))
            if not "www" in page and not 'v=' in page:
                self.pages.append(page.replace('&amp;','&'))
            
            
            # for link in pglink.xpath('.//a'):
                
                # if "pg=" in link.extract() and not "> Next <" in link.extract():
                    # lnk = re.findall(r'href="([a-zA-Z/\.\?0-9=&;]*)', link.extract())
                    # if lnk[0].replace('&amp;','&') not in self.pages:
                        # print(lnk[0].replace('&amp;','&'))
                        # self.pages.append(lnk[0].replace('&amp;','&'))
        
        self.pages = list(set(self.pages))
        # print('List of pages in category')
        for line in self.pages:
            if not "www" in line:
                # print(line)
                assert True
            else:
                self.pages.remove(line)
                       
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