from bs4 import BeautifulSoup
import urllib2
import os
import re
from piecepriceguide import *
import time

f = open('F:/sets/piecesales.txt','r')
outsales = open('F:/sets/piecesalesreal.txt','w')
outinv = open('F:/sets/pieceinv.txt','w')


for line in f:
    if "AVAILABLE" in line:
        outinv.write(line)
    else:
        outsales.write(line)
        
outsales.close()
outinv.close()