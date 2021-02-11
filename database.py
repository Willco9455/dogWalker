## imports the sqlite3 functionality which allows you to create and query local databases
import sqlite3

'''Database Sturcture:

user(userID(PK), username, password)


'''

## This the calss for the databse object that will be imported and used in the main appliation
class dbClass:
    ## function that runs when the database object is first created 
    def __init__(self):
        ## Will connect to main.db if it already exists and will create an empty database with that name if it doesnt
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
            pass

    ## This function will be used to search through specific collumns and return the record that matches the search
    # the two perametres col and search can be null, if they are the function will just return all records in the database
    def search(self, col="null", search="null"):
        ## connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        ## If col peramerter is username then all records where the username matches the search perameter will be 
        # stored in data as an array of arrays
        if col == "username":
            c.execute(f'SELECT * FROM users WHERE username="{search}"')
            data = c.fetchall()
        ## The same goes for if the col perameter is password 
        elif col == "password":
            c.execute(f'SELECT * FROM users WHERE password="{search}"')
            data = c.fetchall() 
        ## If no peramerters are passed into the function then all records are sotred in data variable 
        else:
            c.execute(f'SELECT * FROM users')
            data = c.fetchall()  

        conn.commit()
        conn.close()

        ## Whatever is held in the data variable will be returned from the function 
        return(data)

        
    
    ## This method of the databse object will be used to add new users to the database   
    # the function takes the perameters of usr = the new users username, pas = the new users password 
    def addUsr(self, usr, pas):
        ## Uses the search method of the database to find any users that already have the username passed 
        # into the method 
        srchRes = self.search('username', usr)
        if len(srchRes) != 0: # if there are matching usernames return out of the addUSr method
            print('Username already exists ')
            return 

        ## If there is no existing username in the database then connect to the database and add the user
        #  to the database
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute(f'INSERT INTO users (username, password) VALUES ("{usr}", "{pas}")')

        conn.commit()
        conn.close()

    ## method used to clear the the table to get rid of all records 
    def clrTbl(self):
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        c.execute('DROP TABLE users')
        conn.commit()
        c.execute(''' CREATE TABLE users (
            usrId integer primary key,
            username text,
            password text
            )''')
        conn.commit()

        conn.close()

# db = dbClass()
# while True: 
#     inp = input(': ')
#     if inp == 'clear':
#         db.clrTbl()
#     elif inp == 'show':
#         print(db.search())
