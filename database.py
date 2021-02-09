import sqlite3

'''Database Sturcture:

user(userID(PK), username, password)


'''

## this the calss for the databse object that will be imported and used in the main appliation
class dbClass:
    ## function that runs when the database object is first created 
    def __init__(self):
        ## will connect to main.db if it already exists and will create an empty database with that name if it doesnt
        conn = sqlite3.connect('main.db')
        ## sqlite3 syntax that is used to execute SQL instructions
        c = conn.cursor()

        ## This try and except will create the users table if it doesnt exist and will print table already generated 
        #  if it already exists
        try:
            c.execute(''' CREATE TABLE users (
            usrId integer primary key,
            username text,
            password text
            )''')
            conn.commit()
            conn.close()
        except:
            print('table already genergated')
    



