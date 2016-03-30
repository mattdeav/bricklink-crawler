
f = open('F:/sets/piecesdedup.txt','r')
pieces = []

for piece in f:
    fields = piece.split('|')
    
    pieces.append(fields[0] + '|' + fields[1])
    
f.close()
f2 = open('F:/sets/piecesales.txt','r')
pieces2 = []

for line in f2:
    fields = line.split('|')
    print line
    if fields[0] + '|' + fields[1] not in pieces:
        pieces2.append(fields[0] + '|' + fields[1])
        
for piece in pieces2:
    print piece