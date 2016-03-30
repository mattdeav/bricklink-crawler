

pieces_sales = open('F:\sets\piecesalesreal.txt','r')
colors_list = open('F:\sets\colorscsv.txt','r')
pieces_colors = open('F:\sets\piecescolors.txt','r')
pieces_inv = open('F:\sets\pieceinv.txt','r')

output = open('F:\sets\bricklink_db.txt','w')

sales = []

for line in pieces_sales:
    