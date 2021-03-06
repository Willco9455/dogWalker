## imports the sqlite3 functionality which allows you to create and query local databases
import sqlite3
from flask import url_for

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
            email text,
            password text,
            firstName text,
            lastName text,
            accType text,
            postcode text,
            numberOfReviews integer,
            starRating real,
            profileImage text
            )''')
        except:
            pass
        
        ## creates the availability table if it does not already exist 
        try:
            c.execute(''' CREATE TABLE availability (
            usrId integer,
            day text,
            startTime text,
            endTime text,
            PRIMARY KEY (usrId, day)
            )''')
        except:
            pass
        
        ## creates the booking table if it does not already exist 
        try:
            c.execute(''' CREATE TABLE booking (
            ownerId integer,
            walkerId integer,
            date text,
            day text,
            startTime text,
            endTime text,
            PRIMARY KEY (ownerId, walkerId, date)
            )''')
        except:
            pass

        ## creates the review table if it does not already exist 
        try:
            c.execute(''' CREATE TABLE review (
            byUsrId integer,
            forUsrId integer,
            date text,
            star integer,
            message text,
            PRIMARY KEY (byUsrId, forUsrId, message)
            )''')
        except:
            pass

        ## closes connectrion to database
        conn.commit()
        conn.close()
    

    ## This function will be used to search through specific collumns and return the record that matches the search
    # the two perametres col and search can be null, if they are the function will just return all records in the database
    def search(self, col="null", search="null"):
        ## connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        ## If col peramerter is username then all records where the username matches the search perameter will be 
        # stored in data as an array of arrays
        if col == "email":
            c.execute(f'SELECT * FROM users WHERE email="{search}"')
            data = c.fetchall()
        ## The same goes for if the col perameter is password 
        elif col == "password":
            c.execute(f'SELECT * FROM users WHERE password="{search}"')
            data = c.fetchall() 
        elif col == "usrId":
            c.execute(f'SELECT * FROM users WHERE usrId="{search}"')
            data = c.fetchall() 
        # if collum entered is postcode then an array of users with a matching post code will be returned
        elif col == "postcode":
            c.execute(f'SELECT * FROM users WHERE postcode="{search}"')
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
    # def addUsr(self, email, pas, fName, lName, accType, post, numberOfReviews, starRating):
    def addUsr(self, email, pas, fName, lName, accType, post):
        ## Uses the search method of the database to find any users that already have the username passed 
        # into the method 
        srchRes = self.search('email', email)
        if len(srchRes) != 0: # if there are matching usernames return out of the addUSr method
            print('Username already exists ')
            return 

        ## If there is no existing username in the databaseh then connect to the database and add the user
        #  to the database
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute(f'''INSERT INTO users (email, password, firstName, lastName, accType, postcode, numberOfReviews, starRating, profileImage) 
            VALUES ("{email}", "{pas}", "{fName}", "{lName}", "{accType}", "{post}", 0, 0, "profilePic.png")
            ''')
        print('Account Created !!')
        conn.commit()
        conn.close()

    # Will update the starRating for a user by adding a star 
    def updateRatingAdd(self, usrId, newStar):
        
        ## connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        # gets the current number of review and the current star rating for the userId
        c.execute(f'SELECT numberOfReviews, starRating FROM users WHERE usrId="{usrId}"')
        data = c.fetchall()
        print(data)

        # adds one to the number of reviews made and saves as new variable
        newNumReviews = data[0][0] + 1
        print(newNumReviews)


        # calculates the new mean star rating 
        newStarRating = ((data[0][0] * data[0][1]) + newStar) / newNumReviews
        # rounds the new star rating to the nearest 1/10th
        newStarRating = round(newStarRating, 1)
        print('newstar' + str(newStarRating))
        # update the current number of review and the current star rating
        c.execute(f'UPDATE users SET numberOfReviews = {newNumReviews}, starRating = {newStarRating} WHERE usrId="{usrId}"')
        conn.commit()
        conn.close()

    def updateRatingMinus(self, usrId, oldStar):
        ## connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        # gets the current number of review and the current star rating for the userId
        c.execute(f'SELECT numberOfReviews, starRating FROM users WHERE usrId="{usrId}"')
        data = c.fetchall()

        # adds one to the number of reviews made and saves as new variable
        newNumReviews = data[0][0] - 1


        if newNumReviews == 0:
            c.execute(f'UPDATE users SET numberOfReviews = 0, starRating = 0 WHERE usrId="{usrId}"')
        else:   
            # calculates the new mean star rating 
            newStarRating = ((data[0][0] * data[0][1]) - oldStar) / newNumReviews
            # rounds the new star rating to the nearest 1/10th
            newStarRating = round(newStarRating, 1)
            c.execute(f'UPDATE users SET numberOfReviews = {newNumReviews}, starRating = {newStarRating} WHERE usrId="{usrId}"')
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
            email text,
            password text,
            firstName text,
            lastName text,
            accType text,
            postcode text
            numberOfReviews integer,
            starRating real,
            profileImage text
            )''')
        conn.commit()

        conn.close()

    def changeProfilePic(self, usrId, profileImage):
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
       

        # update the
        c.execute(f'UPDATE users SET profileImage = "{profileImage}" WHERE usrId="{usrId}"')
        conn.commit()
        conn.close()
#####################################################################################################################
################################# START OF AVAILABILITY FUNCTIONALITY ###############################################
#####################################################################################################################

    def clrAvail(self):
        conn = sqlite3.connect('main.db')
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

    # Method that will add an avilability record for one day of one user if there is already a record 
    # there it will replace it 
    def addAvail(self, usrId, day, startTime, endTime):
        ## connects to database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        ## will delete any record that currently has the same usrId and day together 
        self.delAvail(usrId, day)
        # Inserts the new data into the table
        c.execute(f'''
        INSERT INTO availability (usrId, day, startTime, endTime)
        VALUES ({usrId}, "{day}","{startTime}","{endTime}")
        ''')
        conn.commit()
        conn.close()
    
    ''' This method will take in the usrId and will return the availability of that user in the form of an array
               Monday               Tuesday            Wednesday
        [startTime, endTime],[startTime, endTime],[startTime, endTime] , .....etc]
        time will be ['none', 'none'] if there is no record of availability '''
    def getAvail(self, usrId):
        # List of all the days that wil lbe looped throug later 
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        # Empty availability array that will be fileld and returned from the method
        avail = []
        # Loops through all the days
        for i in days:
            # For each day attempt to fetch a record from the database
            try:
                c.execute(f'select * FROM availability WHERE usrId = {usrId} AND day = "{i}"')
                data = c.fetchall() 
                avail.append([[data[0][2]],[data[0][3]]])
            # If there is no record add ['none', 'none'] for that day
            except:
                avail.append(['none', 'none'])
        # Return the avail array from the method
        return(avail)
    
    # Deletes record with the usrId and day that are passwd into the function if there is no match nothing will happen
    def delAvail(self, usrId, day):
        ## connects to database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        ## Checks if there is any data with the same usrId and day already 
        c.execute(f'select * FROM availability WHERE usrId = {usrId} AND day = "{day}"')
        data = c.fetchall() 
        ## if there is data there already then it will remove it from the table otherwise nothing will happen 
        if len(data) > 0:
            c.execute(f'DELETE FROM availability WHERE usrId = {usrId} AND day = "{day}"')
        
        conn.commit()
        conn.close()
    
#####################################################################################################################
################################# START OF BOOKING FUNCTIONALITY ####################################################
#####################################################################################################################

    def clrBooking(self):
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute('DROP TABLE booking')
        conn.commit()
        c.execute(''' CREATE TABLE booking (
            ownerId integer,
            walkerId integer,
            date text,
            day text,
            startTime text,
            endTime text,
            PRIMARY KEY (ownerId, walkerId, date)
            )''')
        conn.commit()

        conn.close()

    # Method takes in infomation about a booking and adds it to the database
    def addBooking(self, ownerId, walkerId, date, day, startTime, endTime):
        ## connects to database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        # Inserts the new data into the table
        c.execute(f'''
        INSERT INTO booking (ownerId, walkerId, date, day, startTime, endTime)
        VALUES ({ownerId},{walkerId},"{date}","{day}","{startTime}","{endTime}")
        ''')
        conn.commit()
        conn.close()
    
    # Takes the walkerId and the day of the booking and will return all the bookings for that day
    def getWalkerBookings(self, walkerId, date='Null'):
        ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        if date == 'Null':
            c.execute(f'SELECT * FROM booking WHERE walkerId="{walkerId}" ORDER BY date ASC')
        else:
            c.execute(f'SELECT * FROM booking WHERE walkerId="{walkerId}" AND date="{date}" ')
        
        # SQL query which will fetch the booksings for the walker
        data = c.fetchall()
        return(data)

        conn.commit()
        conn.close()
    
    def getOwnerBookings(self, ownerId):
        ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        # SQL query which will fetch the booksings for the walker
        c.execute(f'SELECT * FROM booking WHERE ownerId="{ownerId}" ORDER BY date ASC')
        data = c.fetchall()
        return(data)

        conn.commit()
        conn.close()

    def delBooking(self, ownerId, walkerId, date):
        print(str(ownerId) + str(walkerId) + str(date))
        ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute(f'DELETE FROM booking WHERE ownerId={ownerId} and walkerId={walkerId} and date="{date}"')
        conn.commit()
        conn.close()

#####################################################################################################################
################################# START OF REVIEW TABLE FUNCTIONALITY ####################################################
#####################################################################################################################
    
    def clrReview(self):
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute('DROP TABLE review')
        conn.commit()
        c.execute(''' CREATE TABLE review (
            byUsrId integer,
            forUsrId integer,
            date text,
            star integer,
            message text,
            PRIMARY KEY (byUsrId, forUsrId, message)
            )''')
        conn.commit()
        conn.close()

    def makeReview(self, byUsrId, forUsrId, date, star, message):
        ## connects to database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        c.execute(f'SELECT * FROM review WHERE byUsrId="{byUsrId}" AND forUsrId="{forUsrId}"')
        data = c.fetchall()
        if len(data) != 0:
            print('cannot leave two reviews silly billy')
            return 

        # Inserts the new data into the table
        c.execute(f'''
        INSERT INTO review (byUsrId, forUsrId, date, star, message)
        VALUES ({byUsrId},{forUsrId},"{date}","{star}","{message}")
        ''')

        print('booking made successfully')
        conn.commit()
        conn.close()

        # Updates the star rating for the user
        self.updateRatingAdd(forUsrId, star)
    
    def getReviewsFor(self, usrId):
        ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        # SQL query which will fetch the Reviews for the walker
        c.execute(f'SELECT * FROM review WHERE forUsrId="{usrId}" ORDER BY date DESC Limit 5')
        # c.execute(f'SELECT * FROM review ORDER BY date DESC')
        data = c.fetchall()
        return(data)

        conn.commit()
        conn.close()
    
    def getReviewsBy(self, usrId):
         ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()

        # SQL query which will fetch the  for the walker
        c.execute(f'SELECT * FROM review WHERE byUsrId="{usrId}" ORDER BY date DESC')
        data = c.fetchall()
        return(data)

        conn.commit()
        conn.close()
    
    def deleteReview(self, byUsrId, forUsrId, message):
        ## Connects to the database 
        conn = sqlite3.connect('main.db')
        c = conn.cursor()
        c.execute(f'DELETE FROM review WHERE byUsrId={byUsrId} and forUsrId={forUsrId} and message="{message}"')
        print('was deleted')
        conn.commit()
        conn.close()

# db.clrReview()

# print(db.search('usrId', 1))
# db.clrBooking()
# print(db.getReviewsFor(1))

# db.makeReview(3,1, '2021-09-21', 4, 'Great guy had no problems with this walk')
# db.clrReview()
# db.clrTbl()
# db.clrAvail()

# '''

# db = dbClass()
# db.changeProfilePic(2, 'profile3.jpg')
# # Add the test set of data to the database
# db.addUsr('johnsnow@gmail.com','password1','John','Snow','walker','LS29')
# db.addUsr('jamesright@gmail.com','password1','James','Right','owner','TD40')
# db.addUsr('robertsmith@gmail.com','password1','Robert','Smith','owner','LS29')
# db.addUsr('michaelbrown@gmail.com','password1','Michael','Brown','walker','TD40')
# db.addUsr('davidjones@gmail.com','password1','David','Jones','walker','LS29')
# db.addUsr('richarddavis@gmail.com','password1','Richard','Davis','walker','LS29')

# # Add the test set 
# db.addAvail(1,'monday','08:00','17:00')
# db.addAvail(1,'tuesday','08:00','17:00')
# db.addAvail(1,'wednesday','09:30','17:00')
# db.addAvail(1,'thursday','08:00','12:00')
# db.addAvail(1,'friday','08:00','17:00')
# db.addAvail(4,'monday','06:00','15:00')
# db.addAvail(4,'tuesday','06:00','15:00')
# db.addAvail(4,'friday','06:00','15:00')
# db.addAvail(4,'saturday','06:00','15:00')
# db.addAvail(5,'monday','07:00','16:00')
# db.addAvail(5,'tuesday','07:00','16:00')
# db.addAvail(5,'wednesday','07:00','16:00')
# db.addAvail(6,'saturday','12:00','18:00')
# db.addAvail(6,'sunday','12:00','18:00')

# db.addBooking(2,1,'2021-05-03','monday','09:00','10:00')
# db.addBooking(2,1,'2021-05-04','tuesday','13:00','14:00')
# # db.addBooking(3,4,'2021-05-03','monday','07:00','08:00')



# '''