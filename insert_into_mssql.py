import pymssql
import time


def create_piece_table(cursor):
    # PIECE DDL
    piece_ddl = """create table dbo.piece
    (
    PIECE_ID varchar(20),
    COLOR varchar(50),
    TYPE varchar(50),
    NAME varchar(200),
    CONSTRAINT PK_Piece_PieceIDPK PRIMARY KEY CLUSTERED (PIECE_ID,COLOR,TYPE)
    )
    ;"""
    cursor.execute(piece_ddl)


def insert_piece_rows(cursor):
    # PIECE INSERTS
    inputfile = open('F:/sets/piecescolors.txt','r')

    for line in inputfile:
        columns = line.replace('\n','').replace("'","''").split('|')
        if len(columns[1]) > 50:
            columns[1] = 'NULL'
        piece_id = columns[0]
        color = columns[1]
        type = columns[2]
        name = columns[3]
        sql = "IF NOT EXISTS (select 1 from dbo.piece where piece_id = '" + piece_id + "' and color = '" + color + "' and type = '" + type + "') INSERT INTO dbo.piece(PIECE_ID, COLOR, TYPE, NAME) VALUES('" + "', '".join(columns) + "');"
        cursor.execute(sql)

def create_inv_sales(cursor):
    # INV_SALES DDL
    inv_ddl = """create table dbo.inv
    (
    PIECE_ID varchar(20),
    COLOR varchar(50),
    TYPE varchar(50),
    QTY int,
    PRICE decimal(10,2)
    )
    ;"""
    cursor.execute(inv_ddl)
    
    sales_ddl = """create table dbo.sales
    (
    PIECE_ID varchar(20),
    COLOR varchar(50),
    TYPE varchar(50),
    MON varchar(15),
    YEAR varchar(4),
    QTY int,
    PRICE decimal(10,2)
    )
    ;"""
    cursor.execute(sales_ddl)

    
def insert_inv_sales_rows(cursor):
    # # INV_SALES INSERTS
    # inputfile = open('F:/sets/piecesales.txt','r')
    # x=0

    # for line in inputfile:
        # x+=1
        # columns = line.replace('\n','').replace("'","''").split('|')
        # piece_id = columns[0]
        # color = columns[1]
        # type = columns[2]
        # if "AVAILABLE" in type:
            # qty = columns[3]
            # price = columns[4]
            # month = "NA"
            # year = "NA"
            # sql = "INSERT INTO dbo.inv(PIECE_ID, COLOR, TYPE, QTY, PRICE) VALUES('" + piece_id + "', '" + color + "', '" + type + "', '" + qty + "', '" + price + "');"
        # else:
            # month = columns[3]
            # qty = columns[4]
            # price = columns[5]
            # if month == "December":
                # year = time.strftime("%Y") - 1
            # else:
                # year = time.strftime("%Y")
            # sql = "INSERT INTO dbo.sales(PIECE_ID, COLOR, TYPE, MON, YEAR, QTY, PRICE) VALUES('" + piece_id + "', '" + color + "', '" + type + "', '" + month + "', '" + year + "', '" + qty + "', '" + price + "');"
        # # print(sql)
        # if x % 10000 == 0:
            # print("On #" + str(x) + " record")
        
        # cursor.execute(sql)
    sql = "BULK INSERT dbo.sales FROM 'F:/sets/piecesalesreal.txt' WITH (DATAFILETYPE = 'char', FIELDTERMINATOR = '|', ROWTERMINATOR = '\r\n');"
    cursor.execute(sql)
    
    sql = "BULK INSERT dbo.inv FROM 'F:/sets/pieceinv.txt' WITH (DATAFILETYPE = 'char', FIELDTERMINATOR = '|', ROWTERMINATOR = '\r\n');"
    cursor.execute(sql)


def create_colors_table(cursor):
    # COLORS DDL
    colors_ddl = """create table dbo.colors
    (
    COLOR_ID varchar(10),
    COLOR_NAME varchar(50),
    CONSTRAINT PK_Color_ColorID PRIMARY KEY CLUSTERED (COLOR_ID)
    )
    ;"""
    cursor.execute(colors_ddl)


def insert_colors_rows(cursor):
    # COLORS INSERTS
    inputfile = open('F:/sets/colorscsv.txt','r')

    for line in inputfile:
        columns = line.replace('\n','').replace("'","''").split('|')
        color_id = columns[0]
        color_name = columns[1]
        sql = "IF NOT EXISTS (select 1 from dbo.colors where color_id = '" + color_id + "' and color_name = '" + color_name + "') INSERT INTO dbo.colors(color_id, color_name) VALUES('" + "', '".join(columns) + "');"
        cursor.execute(sql)
        
def create_set_table(cursor):
    sets_ddl = """create table dbo.sets
    (
    SET_ID varchar(30),
    SET_NAME varchar(150),
    YEAR_RELEASED VARCHAR(4),
    CATEGORY VARCHAR(50),
    SUBCATEGORY VARCHAR(50),
    WEIGHT DECIMAL(10,2),
    CONSTRAINT PK_Set_SetID PRIMARY KEY CLUSTERED (SET_ID)
    )
    ;"""
    cursor.execute(sets_ddl)


def insert_set_rows(cursor):
    inputfile = open('F:/sets/sets.txt','r')

    for line in inputfile:
        columns = line.replace('\n','').replace("'","''").split('|')
        set_id = columns[0]
        set_name = columns[1]
        year_released = columns[2]
        category = columns[3]
        subcategory = columns[4]
        weight = columns[5].replace('g','')
        columns[5] = columns[5].replace('g','')
        sql = "IF NOT EXISTS (select 1 from dbo.sets where set_id = '" + set_id + "') INSERT INTO dbo.sets(SET_ID, SET_NAME, YEAR_RELEASED, CATEGORY, SUBCATEGORY, WEIGHT) VALUES('" + "', '".join(columns) + "');"
        # print(sql)
        cursor.execute(sql)

def create_setpiece_table(cursor):
    sets_ddl = """create table dbo.setsales
    (
    SET_ID varchar(30),
    PIECE_ID VARCHAR(30),
    COLOR_NAME varchar(50),
    QTY integer,
    
    )
    ;"""
    #CONSTRAINT PK_Setpiece_SetID PRIMARY KEY CLUSTERED (SET_ID,PIECE_ID,COLOR_NAME)
    cursor.execute(sets_ddl)

def insert_setpiece_rows(cursor):
    inputfile = open('F:/sets/setpiecesdedup.txt','r')
    x=0
    for line in inputfile:
        x+=1
        columns = line.replace('\n','').replace("'","''").split('|')
        set_id = columns[0]
        piece_id = columns[1]
        color_name = columns[2]
        
        if ',' in color_name:
            columns[2] = columns[2].split(',')[-1]
        qty = columns[3]
        sql = "INSERT INTO dbo.setpiece(SET_ID, PIECE_ID, COLOR_NAME, QTY) VALUES('" + "', '".join(columns) + "');"
        # print(sql)
        
        # if piece_id == 'sw011':
            # print('this should be inserting!!!')
        
        if x % 10000 == 0:
            print("On row#" + str(x))
        cursor.execute(sql)
        
        
def create_setprice_table(cursor):
    sets_ddl = """create table dbo.setprice
    (
    SET_ID varchar(30),
    PRICE decimal(10,2),
    CONSTRAINT PK_Setprice_SetID PRIMARY KEY CLUSTERED (SET_ID)
    )
    ;"""
    cursor.execute(sets_ddl)

def insert_setprice_rows(cursor):
    inputfile = open('F:/sets/2016to2010prices.txt','r')
    x=0
    for line in inputfile:
        x+=1
        if x > 1:
            columns = line.replace('\n','').replace("'","''").split(',')
            set_id = columns[1]
            
            if columns[2] != '':
                set_id += '-' + columns[2]
            price = columns[10]
            
            if price == '':
                price = '0.0'
            # print(set_id,price)
            select_columns = [set_id,price]
            
            sql = "IF NOT EXISTS (select 1 from dbo.setprice where set_id = '" + set_id + "') INSERT INTO dbo.setprice(SET_ID, PRICE) VALUES('" + "', '".join(select_columns) + "');"
            # print(sql)
            if x % 10000 == 0:
                print("On row#" + str(x))
            cursor.execute(sql)
        
def create_setsales_table(cursor):
    sets_ddl = """create table dbo.setsales
    (
    SET_ID varchar(30),
    PRICE decimal(10,2),
    QTY integer,
    CONSTRAINT PK_setsales_SetID PRIMARY KEY CLUSTERED (SET_ID,PRICE)
    )
    ;"""
    cursor.execute(sets_ddl)
    
    sets_ddl = """create table dbo.setinv
    (
    SET_ID varchar(30),
    PRICE decimal(10,2),
    QTY integer,
    CONSTRAINT PK_setinv_SetID PRIMARY KEY CLUSTERED (SET_ID,PRICE)
    )
    ;"""
    cursor.execute(sets_ddl)

def insert_setsales_rows(cursor):
    inputfile = open('F:/sets/sales.txt','r')
    x=0
    for line in inputfile:
        x+=1
        columns = line.replace('\n','').replace("'","''").split('|')
        set_id = columns[0]
        if 'SALES' in columns[1]:
            price = columns[4]
            qty = columns[3]
            select_columns = [set_id,price,qty]
            sql = "IF NOT EXISTS (select 1 from dbo.setsales where set_id = '" + set_id + "' and price = '" + price + "') INSERT INTO dbo.setsales(SET_ID, PRICE, QTY) VALUES('" + "', '".join(select_columns) + "');"
        else:
            price = columns[3]
            qty = columns[2]
            select_columns = [set_id,price,qty]
            sql = "IF NOT EXISTS (select 1 from dbo.setinv where set_id = '" + set_id + "' and price = '" + price + "') INSERT INTO dbo.setinv(SET_ID, PRICE, QTY) VALUES('" + "', '".join(select_columns) + "');"
        if x % 10000 == 0:
            print("On row#" + str(x))
        cursor.execute(sql)
        
print('testing connection')
conn = pymssql.connect(host='localhost', user='python', password='password')
print('connection opened!')
cursor = conn.cursor()



# create_inv_sales(cursor)
# insert_inv_sales_rows(cursor)

# create_colors_table(cursor)
# insert_colors_rows(cursor)

# create_set_table(cursor)
# insert_set_rows(cursor)

# create_setpiece_table(cursor)
# insert_setpiece_rows(cursor)

# create_setprice_table(cursor)
# insert_setprice_rows(cursor)

create_setsales_table(cursor)
insert_setsales_rows(cursor)

cursor.execute("COMMIT")

# print(cursor.fetchone()[0])
print('closing connection')

conn.close()