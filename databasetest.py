
import sqlite3

## This the calss for the databse object that will be imported and used in the main appliation
class dbClass:
    ## function that runs when the database object is first created 
    def __init__(self):
        ## Will connect to test.db if it already exists and will create an empty database with that name if it doesnt
        conn = sqlite3.connect('test.db')
        ## sqlite3 syntax that is used to execute SQL instructions
        c = conn.cursor()

        ## This try and except will create the users table if it doesnt exist and will print table already generated 
        #  if it already exists
        try:
            c.execute(''' CREATE TABLE availability (
            usrId integer,
            day text,
            startTime text,
            endTime text,
            PRIMARY KEY (usrId, day)
            )''')
            conn.commit()
            conn.close()
        except:
            pass
    
    ## method used to clear the the table to get rid of all records 
    def clrTbl(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('DROP TABLE availability')
        conn.commit()
        c.execute(''' CREATE TABLE availability (
            usrId integer,
            day text,
            startTime text,
            endTime text,
            PRIMARY KEY (usrId, day)
            )''')
        conn.commit()

        conn.close()

    def addAvail(self, usrId, day, startTime, endTime):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute(f'''
        INSERT INTO availability (usrId, day, startTime, endTime)
        VALUES ({usrId}, "{day}","{startTime}","{endTime}")
        ''')
        conn.commit()
        conn.close()

    def getAvail(self, usrId):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()


    def show(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor() 
        c.execute('select * FROM availability WHERE usrId = 5 AND day = "monday"' )
        data = c.fetchall()
        print(data)
        conn.commit()
        conn.close()


db = dbClass()
# db.addAvail(5, 'tuesday', '17:05', '19:00')
db.show()

# db = dbClass()
# while True: 
#     inp = input(': ')
#     if inp == 'clear':
#         db.clrTbl()-
#     elif inp == 'show':
#         print(db.search())