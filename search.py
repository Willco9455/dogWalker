from database import *
import datetime
db = dbClass()

class time:
    # Intiate the variables to give an idea of the variable types
    tString = ''
    tArray = []
    secPastMid = 0
    hours = 0
    mins = 0 
    # Runs when the object is created takes in a time in format 'hh:mm'
    def __init__(self, tString):
        self.tString = tString

        # Splits the string into an array format -> ['HH','MM']
        tArray = tString.split(':')
        # Checks the hours and the minuets in the array for leading 0's and removes them 
        for i in range(0, len(tArray) - 1):
            if tArray[i][0] == "0":
                tArray[i] = tArray[i][1]
        
        # Sets the attribues of the time objects 
        self.tArray = tArray
        self.hours = int(tArray[0])
        self.mins = int(tArray[1])

        # Uses the datatime libray to turn the time into the hours past midnight
        time = datetime.time(self.hours, self.mins)
        seconds = datetime.timedelta(hours=time.hour, minutes=time.minute).total_seconds()
        self.secPastMid = seconds


    # Getter for the secPastMid attribute
    def getSecPastMid(self):
        return(self.secPastMid)

# returns array of valid user objects with 
def search(post, startTime, endTime, date):
    # Turns start and end time into time objects 
    startTimeObj = time(startTime)
    endTimeObj = time(endTime)
    day
    # avaible variable becomes an array of objects with the
    # post code passed into the function (post)
    area = db.search('postcode', post)
    avail = []
    for i in area:
        usrStarTimeObj = i.
        


search('LS29', '08:01', '23:59')



