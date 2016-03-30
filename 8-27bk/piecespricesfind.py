from bs4 import BeautifulSoup
import urllib2
import os
import re
from piecepriceguide import *
import time

def swapcolor(color):
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
            'Mx Clear' : 149,
            'NULL' : 0,
            'The' : 0
        }[color]
    else:
        return "not a color!!!!"


def geturl(piece, color):
    if color > 0:
        return ("http://www.bricklink.com/catalogPG.asp?P=" + piece + "&colorID=" + str(color))
    return ("http://www.bricklink.com/catalogPG.asp?M=" + piece)
    
def htmlclean(self, url):
    soup = BeautifulSoup(url.read())
    temp = ' '.join(soup.prettify().encode('utf-8').split())
    temp = temp.replace('&amp;','&')
    return temp

f = open("F:/sets/sets.txt",'r')
out = open("F:/sets/setsdedup.txt", 'w')

pieces = set()

for line in f:
    if line not in pieces:
        out.write(line)
        pieces.add(line)
        
out.close()
f.close()


# i = 1
# pieces = open("F:/sets/piecesdedup.txt", 'r')

# out = open('F:/sets/pieceprices.txt','w')
# lines = open('F:/sets/piecesales.txt').readlines()
# out = open('F:/sets/piecesales.txt','w')
# startpiece = ""
# startcolor = ""
# for line in reversed(lines):
    # fields = line.split('|')
    # startpiece = fields[0]
    # startcolor = fields[1]
    # break
    
# print startpiece, startcolor
# currentpiece = ""
# currentcolor = ""
# lastpiece = ""
# lastcolor = ""

# for line in lines:
    # if startpiece not in line:
        # out.write(line)
        # fields = line.split('|')
        # currentpiece = fields[0]
        # currentcolor = fields[1]
        
        # if not currentpiece == lastpiece:
            # i = i + 1
        # lastpiece = currentpiece
        # lastcolor = currentcolor
# out.close()
# #print lastpiece, lastcolor
# started = False

# # started = True

# for piece in pieces:
    # if not started:
        # fields = piece.split('|')
        # currpiece = fields[0]
        # #print piece, fields[1]
        # currcolor = str(swapcolor(fields[1]))
        # if currpiece == startpiece:
            # print currpiece, currcolor
        # if currpiece == startpiece and currcolor == startcolor:
            # started = True
            # print "Starting!!"
        # # if startpiece in piece:
            # # started = True
            # # print "starting", piece
    # if started:
        # fields = piece.split('|')
        
        # print str(i) + " - " + fields[0] + " - " + fields[1] + ", " + str(swapcolor(fields[1])) + " - " + fields[2] + " - " + fields[3]
        # url = geturl(fields[0], swapcolor(fields[1]))
        # priceguide(url, fields[0], swapcolor(fields[1]))
        # i = i + 1
        # #time.sleep(1)