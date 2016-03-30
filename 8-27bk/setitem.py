# -*- coding: utf-8 -*-
import re
from priceguide import *
from bs4 import BeautifulSoup
import urllib2
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
from unidecode import unidecode

class setitem(object):
    def __init__(self, catalogpage, subcatname):
        self.catalogpage = catalogpage
        self.instpage = ''
        self.subcatname = subcatname
        setpageurl = self.openurl(self.catalogpage)
        setpagecontent = self.htmlclean(setpageurl)
        
        setsfile = open("F:/sets/sets.txt", 'a')
        
        selector = Selector(response=HtmlResponse(url=self.catalogpage, body=setpagecontent))
        findweight = selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[3]/tr/td/table/tr/td[4]/text()').extract()
        try:
            self.weight = float(''.join(findweight).strip())
        except ValueError:
            self.weight = 0
        print(catalogpage)
        
        # these must have changed?
        # catname = selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table/tr/td/table/tr/td/b/font/a[3]').extract()
        # setname = selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[2]/tr/td/center/font/b').extract()
        
        catname = selector.xpath('//a[contains(@href, "catalogList")]/text()').extract()
        setname = selector.xpath('//span[contains(@id, "item-name-title")]/text()').extract()
        print(setname)
        
        self.setname = re.findall(r'> ([\(\)\w+0-9,\\ #\-\.&;\:\/\'\{\}\!\?]*) <',unidecode(setname[0]))[0]
        self.category = re.findall(r'\"> ([\(\)a-zA-Z0-9 \-\.&;\:\/\'\{\}]*) <',catname[0])[0]
        invpage = re.findall(r'(\/catalogItemInv.*?)">', setpagecontent)
        if len(invpage) > 0:
            self.invpage = re.findall(r'(\/catalogItemInv.*?)">', setpagecontent)[0]
        else:
            self.invpage = ''
        self.pricepage = re.findall(r'"> Inv.*?(/catalogPG.*?)"', setpagecontent)
        
        year = ''
        setnum = ''
        self.year = '0'
        for item in selector.xpath('/html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[3]/tr/td/table/tr'):
            year = re.findall(r'itemYear=([0-9][0-9][0-9][0-9])',item.extract().encode('utf-8'))
            if len(year) > 0:
                self.year = year[0]
            setnum = re.findall(r'Item No: </font> <br> ([a-zA-Z0-9\-\.]*) ',item.extract().encode('utf-8'))
            if len(setnum) > 0:
                self.setnum = setnum[0]
        
        # MAYBE IMPLEMENT LATER
        # instpage = re.findall(r'(\/catalogItem\.asp\?I=[0-9\-]*)">', setpagecontent)
        # if len(instpage) > 0:
            # self.instpage = "/catalogPG.asp?I=" + self.itemnum
        # else:
            # self.instpage = ''
            
        print self.year, self.setnum, self.setname, self.category, self.weight
        setsfile.write(self.setnum + "|" + self.setname + "|" + self.year + "|" + self.category + "|"  + self.subcatname + "|" + str(self.weight) + "\n")
        setsfile.close()
        self.findinvandpricepages()
        #self.getprices()
        
    def __str__(self):
        return (self.category.strip() + ", " + self.setnum + ", " + self.setname + ", " + self.year + ", " + str(self.weight) + ", " + self.catalogpage)
     

    def htmlclean(self, url):
        soup = BeautifulSoup(url.read())
        temp = ' '.join(soup.prettify().encode('utf-8').split())
        temp = temp.replace('&amp;','&')
        return temp
        
    def openurl(self, new):
        return urllib2.urlopen("http://www.bricklink.com" + new)
    
    def swapcolor(self,color):
        if color.__class__ == (1).__class__:
            return{
                1 : 'White',
                49 : 'Very Light Gray',
                99 : 'Very Light Bluish Gray',
                86 : 'Light Bluish Gray',
                9 : 'Light Gray',
                10 : 'Dark Gray',
                85 : 'Dark Bluish Gray',
                11 : 'Black',
                59 : 'Dark Red',
                5 : 'Red',
                27 : 'Rust',
                25 : 'Salmon',
                26 : 'Light Salmon',
                58 : 'Sand Red',
                88 : 'Reddish Brown',
                8 : 'Brown',
                120 : 'Dark Brown',
                69 : 'Dark Tan',
                2 : 'Tan',
                90 : 'Light Flesh',
                28 : 'Flesh',
                150 : 'Medium Dark Flesh',
                91 : 'Dark Flesh',
                106 : 'Fabuland Brown',
                160 : 'Fabuland Orange',
                29 : 'Earth Orange',
                68 : 'Dark Orange',
                4 : 'Orange',
                31 : 'Medium Orange',
                110 : 'Bright Light Orange',
                32 : 'Light Orange',
                96 : 'Very Light Orange',
                3 : 'Yellow',
                103 : 'Bright Light Yellow',
                33 : 'Light Yellow',
                35 : 'Light Lime',
                158 : 'Yellowish Green',
                76 : 'Medium Lime',
                34 : 'Lime',
                155 : 'Olive Green',
                80 : 'Dark Green',
                6 : 'Green',
                36 : 'Bright Green',
                37 : 'Medium Green',
                38 : 'Light Green',
                48 : 'Sand Green',
                39 : 'Dark Turquoise',
                40 : 'Light Turquoise',
                41 : 'Aqua',
                152 : 'Light Aqua',
                63 : 'Dark Blue',
                7 : 'Blue',
                153 : 'Dark Azure',
                156 : 'Medium Azure',
                42 : 'Medium Blue',
                72 : 'Maersk Blue',
                105 : 'Bright Light Blue',
                62 : 'Light Blue',
                87 : 'Sky Blue',
                55 : 'Sand Blue',
                97 : 'Blue-Violet',
                109 : 'Dark Blue-Violet',
                43 : 'Violet',
                73 : 'Medium Violet',
                44 : 'Light Violet',
                89 : 'Dark Purple',
                24 : 'Purple',
                93 : 'Light Purple',
                157 : 'Medium Lavender',
                154 : 'Lavender',
                54 : 'Sand Purple',
                71 : 'Magenta',
                47 : 'Dark Pink',
                94 : 'Medium Dark Pink',
                104 : 'Bright Pink',
                23 : 'Pink',
                56 : 'Light Pink',
                12 : 'Trans-Clear',
                13 : 'Trans-Black',
                17 : 'Trans-Red',
                18 : 'Trans-Neon Orange',
                98 : 'Trans-Orange',
                121 : 'Trans-Neon Yellow',
                19 : 'Trans-Yellow',
                16 : 'Trans-Neon Green',
                108 : 'Trans-Bright Green',
                20 : 'Trans-Green',
                14 : 'Trans-Dark Blue',
                74 : 'Trans-Medium Blue',
                15 : 'Trans-Light Blue',
                113 : 'Trans-Very Lt Blue',
                114 : 'Trans-Light Purple',
                51 : 'Trans-Purple',
                50 : 'Trans-Dark Pink',
                107 : 'Trans-Pink',
                21 : 'Chrome Gold',
                22 : 'Chrome Silver',
                57 : 'Chrome Antique Brass',
                122 : 'Chrome Black',
                52 : 'Chrome Blue',
                64 : 'Chrome Green',
                82 : 'Chrome Pink',
                83 : 'Pearl White',
                119 : 'Pearl Very Light Gray',
                66 : 'Pearl Light Gray',
                95 : 'Flat Silver',
                77 : 'Pearl Dark Gray',
                78 : 'Metal Blue',
                61 : 'Pearl Light Gold',
                115 : 'Pearl Gold',
                81 : 'Flat Dark Gold',
                84 : 'Copper',
                67 : 'Metallic Silver',
                70 : 'Metallic Green',
                65 : 'Metallic Gold',
                60 : 'Milky White',
                159 : 'Glow in Dark White',
                46 : 'Glow In Dark Opaque',
                118 : 'Glow In Dark Trans',
                101 : 'Glitter Trans-Clear',
                102 : 'Glitter Trans-Purple',
                100 : 'Glitter Trans-Dark Pink',
                111 : 'Speckle Black-Silver',
                151 : 'Speckle Black-Gold',
                116 : 'Speckle Black-Copper',
                117 : 'Speckle DBGray-Silver',
                123 : 'Mx White',
                124 : 'Mx Light Bluish Gray',
                125 : 'Mx Light Gray',
                126 : 'Mx Charcoal Gray',
                127 : 'Mx Tile Gray',
                128 : 'Mx Black',
                131 : 'Mx Tile Brown',
                134 : 'Mx Terracotta',
                132 : 'Mx Brown',
                133 : 'Mx Buff',
                129 : 'Mx Red',
                130 : 'Mx Pink Red',
                135 : 'Mx Orange',
                136 : 'Mx Light Orange',
                137 : 'Mx Light Yellow',
                138 : 'Mx Ochre Yellow',
                139 : 'Mx Lemon',
                141 : 'Mx Pastel Green',
                140 : 'Mx Olive Green',
                142 : 'Mx Aqua Green',
                146 : 'Mx Teal Blue',
                143 : 'Mx Tile Blue',
                144 : 'Mx Medium Blue',
                145 : 'Mx Pastel Blue',
                147 : 'Mx Violet',
                148 : 'Mx Pink',
                149 : 'Mx Clear'
            }[color]
        elif color.__class__ == ("String").__class__:
            return{
                'White' : 1,
                'Very Light Gray' : 49,
                'Very Light Bluish Gray' : 99,
                'Light Bluish Gray' : 86,
                'Light Gray' : 9,
                'Dark Gray' : 10,
                'Dark Bluish Gray' : 85,
                'Black' : 11,
                'Dark Red' : 59,
                'Red' : 5,
                'Rust' : 27,
                'Salmon' : 25,
                'Light Salmon' : 26,
                'Sand Red' : 58,
                'Reddish Brown' : 88,
                'Brown' : 8,
                'Dark Brown' : 120,
                'Dark Tan' : 69,
                'Tan' : 2,
                'Light Flesh' : 90,
                'Flesh' : 28,
                'Medium Dark Flesh' : 150,
                'Dark Flesh' : 91,
                'Fabuland Brown' : 106,
                'Fabuland Orange' : 160,
                'Earth Orange' : 29,
                'Dark Orange' : 68,
                'Orange' : 4,
                'Medium Orange' : 31,
                'Bright Light Orange' : 110,
                'Light Orange' : 32,
                'Very Light Orange' : 96,
                'Yellow' : 3,
                'Bright Light Yellow' : 103,
                'Light Yellow' : 33,
                'Light Lime' : 35,
                'Yellowish Green' : 158,
                'Medium Lime' : 76,
                'Lime' : 34,
                'Olive Green' : 155,
                'Dark Green' : 80,
                'Green' : 6,
                'Bright Green' : 36,
                'Medium Green' : 37,
                'Light Green' : 38,
                'Sand Green' : 48,
                'Dark Turquoise' : 39,
                'Light Turquoise' : 40,
                'Aqua' : 41,
                'Light Aqua' : 152,
                'Dark Blue' : 63,
                'Blue' : 7,
                'Dark Azure' : 153,
                'Medium Azure' : 156,
                'Medium Blue' : 42,
                'Maersk Blue' : 72,
                'Bright Light Blue' : 105,
                'Light Blue' : 62,
                'Sky Blue' : 87,
                'Sand Blue' : 55,
                'Blue-Violet' : 97,
                'Dark Blue-Violet' : 109,
                'Violet' : 43,
                'Medium Violet' : 73,
                'Light Violet' : 44,
                'Dark Purple' : 89,
                'Purple' : 24,
                'Light Purple' : 93,
                'Medium Lavender' : 157,
                'Lavender' : 154,
                'Sand Purple' : 54,
                'Magenta' : 71,
                'Dark Pink' : 47,
                'Medium Dark Pink' : 94,
                'Bright Pink' : 104,
                'Pink' : 23,
                'Light Pink' : 56,
                'Trans-Clear' : 12,
                'Trans-Black' : 13,
                'Trans-Red' : 17,
                'Trans-Neon Orange' : 18,
                'Trans-Orange' : 98,
                'Trans-Neon Yellow' : 121,
                'Trans-Yellow' : 19,
                'Trans-Neon Green' : 16,
                'Trans-Bright Green' : 108,
                'Trans-Green' : 20,
                'Trans-Dark Blue' : 14,
                'Trans-Medium Blue' : 74,
                'Trans-Light Blue' : 15,
                'Trans-Very Lt Blue' : 113,
                'Trans-Light Purple' : 114,
                'Trans-Purple' : 51,
                'Trans-Dark Pink' : 50,
                'Trans-Pink' : 107,
                'Chrome Gold' : 21,
                'Chrome Silver' : 22,
                'Chrome Antique Brass' : 57,
                'Chrome Black' : 122,
                'Chrome Blue' : 52,
                'Chrome Green' : 64,
                'Chrome Pink' : 82,
                'Pearl White' : 83,
                'Pearl Very Light Gray' : 119,
                'Pearl Light Gray' : 66,
                'Flat Silver' : 95,
                'Pearl Dark Gray' : 77,
                'Metal Blue' : 78,
                'Pearl Light Gold' : 61,
                'Pearl Gold' : 115,
                'Flat Dark Gold' : 81,
                'Copper' : 84,
                'Metallic Silver' : 67,
                'Metallic Green' : 70,
                'Metallic Gold' : 65,
                'Milky White' : 60,
                'Glow in Dark White' : 159,
                'Glow In Dark Opaque' : 46,
                'Glow In Dark Trans' : 118,
                'Glitter Trans-Clear' : 101,
                'Glitter Trans-Purple' : 102,
                'Glitter Trans-Dark Pink' : 100,
                'Speckle Black-Silver' : 111,
                'Speckle Black-Gold' : 151,
                'Speckle Black-Copper' : 116,
                'Speckle DBGray-Silver' : 117,
                'Mx White' : 123,
                'Mx Light Bluish Gray' : 124,
                'Mx Light Gray' : 125,
                'Mx Charcoal Gray' : 126,
                'Mx Tile Gray' : 127,
                'Mx Black' : 128,
                'Mx Tile Brown' : 131,
                'Mx Terracotta' : 134,
                'Mx Brown' : 132,
                'Mx Buff' : 133,
                'Mx Red' : 129,
                'Mx Pink Red' : 130,
                'Mx Orange' : 135,
                'Mx Light Orange' : 136,
                'Mx Light Yellow' : 137,
                'Mx Ochre Yellow' : 138,
                'Mx Lemon' : 139,
                'Mx Pastel Green' : 141,
                'Mx Olive Green' : 140,
                'Mx Aqua Green' : 142,
                'Mx Teal Blue' : 146,
                'Mx Tile Blue' : 143,
                'Mx Medium Blue' : 144,
                'Mx Pastel Blue' : 145,
                'Mx Violet' : 147,
                'Mx Pink' : 148,
                'Mx Clear' : 149
            }[color]
        else:
            return "not a color!!!!"
    
    def findinvandpricepages(self):
        piecesfile = open("F:/sets/pieces.txt", 'a')
        setpiecesfile = open("F:/sets/setpieces.txt", 'a')
        print "start findinvandetc"
        if len(self.invpage) > 0:
            invpage = self.openurl(self.invpage)
            invcontent = self.htmlclean(invpage)
            typetracker = 0
            typepiece = 0
            parts = []
            selector = Selector(response=HtmlResponse(url=self.invpage, body=invcontent))
            
            # GETTING PIECE DATA
            for piece in selector.xpath('//html/body/center/table[3]/tr/td/table/tr/td/table/tr/td/table[2]/tr/td/center/form/table/tr'):
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
                    piezo = piece.xpath('td[3]/a/text()').extract()
                    if len(piezo) > 0:
                        parttype = re.findall(r'catString.*?> ([\(\)a-zA-Z, \']*)',piece.extract().encode('utf-8'))
                        partname = re.findall(r'Name: ([a-zA-Z, \*<>÷=\\\-0-9&\'\(\)/\.\+\/#\:\{\}£\$¥]*)',unidecode(piece.extract().encode('utf-8').replace('&amp;','&')).replace('$?','').replace('&lt;','<').replace('&gt;','>').replace('A*','/').replace('}',')'))
                        
                        #print partname, parttype
                        numpieces = re.findall(r'> ([0-9]*) <', piece.extract().encode('utf-8'))[0]
                        #partcolor = re.findall(r'> ([\-a-zA-Z, 0-9]*?) ' + partname[0].strip().encode('utf-8'),unidecode(piece.extract().encode('utf-8').replace('&amp;','&')).replace('$?','').replace('&lt;','<').replace('&gt;','>').replace('A*','/').replace('}',')'))
                        partcolor = re.findall(r'> ([\-a-zA-Z, 0-9]*?) ' + partname[0].split('{')[0].split('(')[0].split('/')[0].split('-')[0].strip().encode('utf-8'),unidecode(piece.extract().encode('utf-8').replace('&amp;','&')).replace('$?','').replace('&lt;','<').replace('&gt;','>').replace('A*','/').replace('}',')'))
                        
                        #print partname, partcolor, numpieces
                        
                        if len(partcolor) > 0:
                            piecesfile.write(piezo[0].encode('utf-8').strip() + "|" + partcolor[0].strip() + "|" + parttype[0].strip() + "|" + partname[0].strip() +"\n")
                            setpiecesfile.write(self.setnum + "|" + piezo[0].encode('utf-8').strip() + "|" + partcolor[0].strip() + "|" + numpieces + "\n")
                        else:
                            piecesfile.write(piezo[0].encode('utf-8').strip() + "|NULL| " + parttype[0].strip() + "|" + partname[0].strip() + "\n")
                            setpiecesfile.write(self.setnum + "|" + piezo[0].encode('utf-8').strip() + "|NULL|" + numpieces + "\n")
                        # parttype[0].strip() "Brick" "Brick, Modified"
                        # piezo[0].encode('utf-8').strip() is partnum
            time.sleep(1)
        setpiecesfile.close()
        piecesfile.close()
        
    def getprices(self):
        if len(self.pricepage) > 0:
            # RUN PRICEGUIDE (1 iteration)
            self.prices = setpriceguide(self)