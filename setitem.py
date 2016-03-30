#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from priceguide import *
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
from time import strftime
from unidecode import unidecode
from translatecolors import *

class setitem(object):
    def __init__(self, catalogpage, subcatname):
        self.catalogpage = catalogpage
        self.instpage = ''
        self.subcatname = subcatname
        setpageurl = self.openurl(self.catalogpage)
        setpagecontent = self.htmlclean(setpageurl)
        
        setsfile = open("F:/sets/sets.txt", 'a')
        
        selector = Selector(response=HtmlResponse(url=self.catalogpage, body=setpagecontent))
        
        self.category = selector.xpath('//a[contains(@href, "catalogList")]/text()').extract()[0].strip()
        self.setname = selector.xpath('//span[contains(@id, "item-name-title")]/text()').extract()[0].strip()
        self.setname = unidecode(self.setname)
        
        findweight = selector.xpath('//span[contains(@id, "item-weight-info")]/text()').extract()[0].strip()
        if findweight == '?':
            self.weight = 0
        else:
            self.weight = findweight
        
        invpage = re.findall(r'(\/catalogItemInv.*?)">', setpagecontent)
        if len(invpage) > 0:
            self.invpage = 'http://www.bricklink.com' + re.findall(r'(\/catalogItemInv.*?)">', setpagecontent)[0]
        else:
            self.invpage = ''
        
        self.pricepage = re.findall(r'"> Inv.*?(/catalogPG.*?)"', setpagecontent)
        
                
        self.year = selector.xpath('//a[contains(@href, "itemYear=")]/text()').extract()
        if len(self.year) > 0:
            self.year = self.year[0].strip()
        else:
            self.year = '0'
        self.setnum = catalogpage.split('S=')[1].strip()
        self.pricepage = 'catalogPG.asp?S=' + self.setnum
        
        setsfile.write(self.setnum + "|" + self.setname + "|" + self.year + "|" + self.category + "|"  + self.subcatname + "|" + str(self.weight) + "\n")
        setsfile.close()
        
        #uncomment the next line - COMMENTING OUT BECAUSE SETSALES ONLY NEEDS A REFRESH
        # self.findinvandpricepages()
        self.getprices()
        
    def __str__(self):
        return (self.category.strip() + ", " + self.setnum + ", " + self.setname + ", " + self.year + ", " + str(self.weight) + ", " + self.catalogpage)
     

    def htmlclean(self, url):
        soup = BeautifulSoup(url.read())
        temp = ' '.join(soup.prettify().encode('utf-8').split())
        temp = temp.replace('&amp;','&')
        return temp
        
    def openurl(self, new):
        for attempt in range(10):
            try:
                # return urllib2.urlopen("http://www.bricklink.com/" + new)
                return urllib2.urlopen(new)
            except:
                print('Connect attempt failed for ' + new + '. Retrying')
                time.sleep(10)
                continue
        # return urllib2.urlopen("http://alpha.bricklink.com/pages/clone/" + new)
    
    def findinvandpricepages(self):
        setpiecesfile = open("F:/sets/setpieces.txt", 'a')
        piecesfile = open("F:/sets/pieces.txt", 'a')
        
        if len(self.invpage) > 0:
            invpage = self.openurl(self.invpage)
            invcontent = self.htmlclean(invpage)
            typetracker = 0
            typepiece = 0
            parts = []
            selector = Selector(response=HtmlResponse(url=self.invpage, body=invcontent))
            
            # GETTING PIECE DATA
            # for piece in selector.xpath('//html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[2]/tr/td/center/form/table/tr'):
            # for piece in selector.xpath('//table[contains(@class, "ta")]/text()'):
            for piece in selector.xpath('//html/body/center/table/tr[1]/td/table[2]/tr/td/center/form/table/tr'):
                if "REGULAR ITEMS:" in piece.extract().encode('utf-8').upper():
                    typetracker = 1
                elif "EXTRA ITEMS:" in piece.extract().encode('utf-8').upper():
                    typetracker = 2
                elif "COUNTERPARTS:" in piece.extract().encode('utf-8').upper():
                    typetracker = 3
                elif "ALTERNATE ITEMS:" in piece.extract().encode('utf-8').upper():
                    typetracker = 4
                elif "PARTS:" in piece.extract().encode('utf-8').upper():
                    typepiece = 1
                elif "MINIFIGS:" in piece.extract().encode('utf-8').upper():
                    typepiece = 2
                elif "SETS:" in piece.extract().encode('utf-8').upper():
                    typepiece = 0
                elif not typepiece == 0:
                    # checking for Item No.
                    # piezo = piece.xpath('td[3]/a/text()').extract()
                    piezo = piece.xpath('td[3]/a/text()').extract()
                    
                    if len(piezo) > 0:
                        parttype = re.findall(r'catString.*?> ([\(\)a-zA-Z, \']*)',piece.extract().encode('utf-8'))
                        partname = re.findall(r'Name: ([a-zA-Z, \*<>÷=\\\-0-9&\'\(\)/\.\+\/#\:\{\}£\$¥]*)',unidecode(piece.extract().encode('utf-8').replace('&amp;','&')).replace('$?','').replace('&lt;','<').replace('&gt;','>').replace('A*','/').replace('}',')'))
                        numpieces = re.findall(r'> ([0-9]*) <', piece.extract().encode('utf-8'))[0]
                        partcolor = re.findall(r'> ([\-a-zA-Z, 0-9]*?) ' + partname[0].split('{')[0].split('(')[0].split('/')[0].split('-')[0].strip().encode('utf-8'),unidecode(piece.extract().encode('utf-8').replace('&amp;','&')).replace('$?','').replace('&lt;','<').replace('&gt;','>').replace('A*','/').replace('}',')'))
                        
                        if len(partcolor) > 0:
                            piecesfile.write(piezo[0].encode('utf-8').strip() + "|" + partcolor[0].strip() + "|" + parttype[0].strip() + "|" + partname[0].strip() +"\n")
                            setpiecesfile.write(self.setnum + "|" + piezo[0].encode('utf-8').strip() + "|" + partcolor[0].strip() + "|" + numpieces + "\n")
                        else:
                            piecesfile.write(piezo[0].encode('utf-8').strip() + "|NULL| " + parttype[0].strip() + "|" + partname[0].strip() + "\n")
                            setpiecesfile.write(self.setnum + "|" + piezo[0].encode('utf-8').strip() + "|NULL|" + numpieces + "\n")
                        # parttype[0].strip() "Brick" "Brick, Modified"
                        # piezo[0].encode('utf-8').strip() is partnum
            # time.sleep(1)
        setpiecesfile.close()
        piecesfile.close()
        
    def getprices(self):
        if len(self.pricepage) > 0:
            self.prices = setpriceguide(self)