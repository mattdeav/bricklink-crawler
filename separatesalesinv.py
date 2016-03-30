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
        columns = line.split('|')
        
        month = columns[3]
        if month == "December":
            # year = time.strftime("%Y") - 1
            year = '2015'
        else:
            year = time.strftime("%Y")
        out_cols = []
        
        out_cols.append(columns[0])
        out_cols.append(columns[1])
        out_cols.append(columns[2])
        out_cols.append(columns[3])
        out_cols.append(year)
        out_cols.append(columns[4])
        out_cols.append(columns[5])
        outsales.write('|'.join(out_cols))
        
outsales.close()
outinv.close()