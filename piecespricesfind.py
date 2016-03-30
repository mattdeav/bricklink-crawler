# This file is step 2?

from bs4 import BeautifulSoup
import urllib2
import os
import re
from piecepriceguide import *
import time
from translatecolors import *

def geturl(piece, color):
    if color > 0:
        return ('http://www.bricklink.com/catalogPG.asp?P=' + piece + '&colorID=' + str(color))
    return ('http://www.bricklink.com/catalogPG.asp?M=' + piece)
    
def htmlclean(self, url):
    soup = BeautifulSoup(url.read())
    temp = ' '.join(soup.prettify().encode('utf-8').split())
    temp = temp.replace('&amp;','&')
    return temp

def dedup_sets():
    f = open('F:/sets/sets.txt','r')
    out = open('F:/sets/setsdedup.txt', 'w')

    sets = set()

    for line in f:
        if line not in sets:
            out.write(line)
            sets.add(line)
            
    out.close()
    f.close()
    
def dedup_setpieces():
    f = open('F:/sets/setpieces.txt','r')
    out = open('F:/sets/setpiecesdedup.txt', 'w')

    pieces = set()

    for line in f:
        if line not in pieces:
            out.write(line)
            pieces.add(line)
            
    out.close()
    f.close()
    
def dedup_pieces():
    f = open('F:/sets/pieces.txt','r')
    out = open('F:/sets/piecesdedup.txt', 'w')

    pieces = set()

    for line in f:
        if line not in pieces:
            out.write(line)
            pieces.add(line)
            
    out.close()
    f.close()

# uncomment these to run the dedup
# dedup_sets()
# dedup_setpieces()
# dedup_pieces()

# I think this is where I got prices for all pieces...
i = 1


# out = open('F:/sets/pieceprices.txt','w')
startpiece = ''
startcolor = ''
started = False

currentpiece = ''
currentcolor = ''
lastpiece = ''
lastcolor = ''

# try:
lines = open('F:/sets/piecesales.txt').readlines()
if len(lines) == 0:
    started = True
else:
    for line in reversed(lines):
        fields = line.split('|')
        startpiece = fields[0]
        startcolor = fields[1]
        break
        
    out = open('F:/sets/piecesales.txt','w')
    for line in lines:
        if startpiece not in line:
            out.write(line)
            fields = line.split('|')
            currentpiece = fields[0]
            currentcolor = fields[1]
            
            if not currentpiece == lastpiece:
                i = i + 1
            lastpiece = currentpiece
            lastcolor = currentcolor
    out.close()
    
# except:
    # print('piecesales.txt does not exist. Creating.')
    # out = open('F:/sets/piecesales.txt','w')
    # out.close()
    # started = True
    






num_pieces = 0

with open('F:/sets/piecesdedup.txt', 'r') as pieces_file:
    for line in pieces_file:
        num_pieces += 1


pieces = open('F:/sets/piecesdedup.txt', 'r')



x = 0

for piece in pieces:
    x = x + 1
    if not started:
        fields = piece.split('|')
        currpiece = fields[0]
        #print piece, fields[1]
        if fields[1] == 'Ultimate':
            fields[1] = 0
        currcolor = str(swapcolor(fields[1]))
        if currpiece == startpiece:
            print currpiece, currcolor
        if currpiece == startpiece and currcolor == startcolor:
            started = True
            print 'Starting!!'
        # if startpiece in piece:
            # started = True
            # print 'starting', piece
    if started:
        fields = piece.split('|')
        if fields[1] == 'Ultimate':
            fields[1] = 0
        # print(str(i) + ' - ' + fields[0] + ' - ' + fields[1] + ', ' + str(swapcolor(fields[1])) + ' - ' + fields[2] + ' - ' + fields[3])
        # print('Reading piece #' + str(x) + ' of ' + str(num_pieces) + '. Color = ' + fields[1])
        # print(fields)
        print('Reading piece #' + str(i) + ' of ' + str(num_pieces) + '.')
        url = geturl(fields[0], swapcolor(fields[1]))
        priceguide(url, fields[0], swapcolor(fields[1]))
        i = i + 1
        time.sleep(5)