from bs4 import BeautifulSoup
import urllib2
import os
import re
import time
from time import strftime
from setitem import *

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class qtyprice(object):

    def __init__(self, qty, price):
        self.qty = qty
        self.price = price
        
    def __str__(self):
        return (self.qty + "|" + self.price)

        
def swapmonth(month):
    if month.__class__ == (1).__class__:
        return{
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September', 
        10 : 'October',
        11 : 'November',
        12 : 'December'
        }[month]
    elif month.__class__ == ("String").__class__:
        return{
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9, 
        'October' : 10,
        'November' : 11,
        'December' : 12
        }[month]
    else:
        return "not a month!!!!"

def isdate(str):
    if len(str) > 5:
        try:
            int(str[len(str)-4:len(str)])
            if "January" in str or "February" in str or "March" in str or "April" in str or "May" in str or "June" in str or "July" in str or "August" in str or "September" in str or "October" in str or "November" in str or "December" in str:
                return True
            return False
        except ValueError:
            return False
        return False
    return False
    
def iscurrency(str):
    item = re.findall(r'([0-9]*?\.[0-9].)',str.encode('utf8','replace'))
    if len(item) > 0:
        return True
    return False

def getcurrency(str):    
    
    return re.findall(r'([0-9]*?\.[0-9].)',str.encode('utf8','replace'))[0]
    
# def isitemqty(str, str2):
    # item = re.findall(r'([0-9]*?)',str.encode('utf8','replace'))
    # if len(item) > 0 and not "Qty" :
        # return True
    # return False

#"http://www.bricklink.com/catalogPG.asp?M=sh073"
class setpriceguide(object):
    def __init__(self, itemset):
        # self.url = urllib2.urlopen("http://www.bricklink.com" + itemset.pricepage[0])
        
        for attempt in range(10):
            try:
                self.url = urllib2.urlopen("http://www.bricklink.com/" + itemset.pricepage)
            except:
                print('Connect attempt failed. Retrying')
                time.sleep(10)
                continue
        
        soup = BeautifulSoup(self.url.read())
        firstitempage = ' '.join(soup.prettify().encode('UTF-8').split())
        firstitempage = firstitempage.replace('&amp;','&')

        self.response = HtmlResponse(url=itemset.catalogpage, body=firstitempage)

        selector = Selector(response=self.response)

        # for item in selector.xpath('//tr/td/text()'):
            # print item.extract()
        # print selector.xpath('//html/body/center/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr[4]/td').extract()
        #/html/body/center/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr[4]/td
        
        newsold = {}
        usedsold = {}

        new = []
        used = []
        #f = open("F:/Users/SUPERB/Dropbox/bricklinkcrawler/sets/setlist.txt", 'w')
        filepath = "F:/sets/sales.txt"

        currentmonth = 0
        currentmontharray = []

        # 1 = newsold, 2 = usedsold, 3 = new, 4 = used
        typetracker = 0
        previtem = ""


        # ALWAYS REMOVE TBODY
        # /html/body/center/table/tr[1]/td/table[3]/tr[4]
        # for table in selector.xpath('//html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[3]/tr[4]'):
        for table in selector.xpath('//html/body/center/table/tr[1]/td/table[3]/tr[4]'):
            reg = re.findall(r'> ([^<]*?) <', table.extract())
            for item in reg:
                item = item.replace(',','')
                if isdate(item):
                    if typetracker == 1:
                        newsold[currentmonth] = currentmontharray
                        currentmontharray = []
                    elif typetracker == 2:
                        usedsold[currentmonth] = currentmontharray
                        currentmontharray = []
                    if swapmonth(item[0:len(item)-5].strip().encode('utf8','replace')) > currentmonth:            
                        #switchitemtype
                        typetracker = typetracker + 1
                    currentmonth = swapmonth(item[0:len(item)-5].strip().encode('utf8','replace'))
                
                elif item.strip() == "Currently Available":
                    if typetracker == 1:
                        newsold[currentmonth] = currentmontharray
                        currentmontharray = []
                        typetracker = 3
                    elif typetracker == 2:
                        usedsold[currentmonth] = currentmontharray
                        currentmontharray = []
                        typetracker = 3
                    elif typetracker == 3:
                        new = currentmontharray
                        currentmontharray = []
                        typetracker = 4
                    elif typetracker == 4:
                        used = currentmontharray
                elif not "Qty" in previtem and not "Price" in previtem and not "Sold" in previtem and not "Lots" in previtem:
                    if iscurrency(item.strip()):
                        currentmontharray.append(qtyprice(previtem.encode('utf8','replace').strip(),getcurrency(item.strip())))
                previtem = item
            if typetracker == 4:
                used = currentmontharray
            else:
                new = currentmontharray
        
        
        if len(newsold) > 0:        
            for monthkey in newsold:
                # f.write(swapmonth(monthkey))
                # f.write("\n")
                for entry in newsold[monthkey]:
                    with open(filepath, 'a') as myfile:
                        myfile.write(itemset.setnum + "|NEWSALES|" + swapmonth(monthkey) + "|" + str(entry) + "\n")
            #f.write("\n")    

        if len(usedsold) > 0:        
            # f.write("UsedSold\n")
            for monthkey in usedsold:
                # f.write(swapmonth(monthkey))
                # f.write("\n")
                for entry in usedsold[monthkey]:
                    with open(filepath, 'a') as myfile:
                        myfile.write(itemset.setnum + "|USEDSALES|" + swapmonth(monthkey) + "|" + str(entry) + "\n")
            #f.write("\n")   

        if len(new) > 0:
            # f.write("NewAvailable\n")
            for item in new:
                with open(filepath, 'a') as myfile:
                        myfile.write(itemset.setnum + "|NEWAVAILABLE|" + str(item) + "\n")
            #f.write("\n")
            
        if len(used) > 0:
            # f.write("UsedAvailable\n")
            for item in used:
                with open(filepath, 'a') as myfile:
                        myfile.write(itemset.setnum + "|USEDAVAILABLE|" + str(item) + "\n")
            #f.write("\n")
            
        #f.close()