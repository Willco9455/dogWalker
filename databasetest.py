
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

    # Method that will add an avilability record for one day of one user if there is already a record there it will replace it 
    def addAvail(self, usrId, day, startTime, endTime):
        ## connects to database 
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        ## will delete
        self.delAvail(usrId, day)
        c.execute(f'''
        INSERT INTO availability (usrId, day, startTime, endTime)
        VALUES ({usrId}, "{day}","{startTime}","{endTime}")
        ''')
        conn.commit()
        conn.close()

    ## this method will take in the usrId of any user whithin the database and will 
    def getAvail(self, usrId):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        avail = []
        for i in days:
            try:
                c.execute(f'select * FROM availability WHERE usrId = {usrId} AND day = "{i}"')
                data = c.fetchall() 
                avail.append([[data[0][2]],[data[0][3]]])
            except:
                avail.append(['none', 'none'])
        
        print(avail)
        return(avail)

    def delAvail(self, usrId, day):
        ## connects to database 
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        ## will delete the record with the usrId and the same day if there is one
        c.execute(f'select * FROM availability WHERE usrId = {usrId} AND day = "{day}"')
        data = c.fetchall() 
        if len(data) > 0:
            c.execute(f'DELETE FROM availability WHERE usrId = {usrId} AND day = "{day}"')
        
        conn.commit()
        conn.close()

    def show(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor() 
        c.execute('select * FROM availability WHERE usrId = 5 ')
        data = c.fetchall()
        print(data)
        conn.commit()
        conn.close()


db = dbClass()
db.addAvail(5, 'saturday', '18:00', '20:00')
db.show()
# db.getAvail(2)

# db = dbClass()
# while True: 
#     inp = input(': ')
#     if inp == 'clear':
#         db.clrTbl()-
#     elif inp == 'show':
#         print(db.search())