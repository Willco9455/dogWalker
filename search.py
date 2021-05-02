from database import *
from user import *
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
        for i in range(0, len(tArray)):
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
    startTime = time(startTime).getSecPastMid()
    endTime = time(endTime).getSecPastMid()
    dayNum = getDay(date)
    # avaible variable becomes an array of objects with the
    # post code passed into the function (post)
    filt1 = db.search('postcode', post)
    filt2 = []
    availabile = []

    # this loop will go through all users with the same post code(filter 1) and will filter out any users 
    # that are not walking at any times on that day  
    for i in range(0, len(filt1)):
        # creates an objec  for the user 
        userObj = user(filt1[i][0])
        # gets the availability of that user
        avail = userObj.getAvail()
        # If the user is availabile then it will be added to the filt2 array 
        if avail[dayNum][0] != 'none':
            filt2.append(filt1[i])

    # Loops through the second filtered users, and will add the valid users to the available array
    for i in range(0, len(filt2)):
        # creates an objec  for the user 
        usrObj = user(filt2[i][0])
        # gets the availability of that user for the specific day
        avail = usrObj.getAvail()[dayNum]
        # gets the start and end times as the seconds past midnight for the current user
        usrStart = time(avail[0][0]).getSecPastMid()
        usrEnd = time(avail[1][0]).getSecPastMid()

        # if the time range for the search is outside of the users time range then skip past this user
        if (startTime < usrStart) or (endTime > usrEnd):
            continue # move onto next i
        
        # if the user has got past these checks then they will be added to the available array
        availabile.append(filt2[i]) 

    # returns an array of all the users that are available
    return availabile


# Take date in as a string in formate -> 'YYYY-MM-DD'
def getDay(date):
    # array of days will be used to turn the day number into a day
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    # turns the date string into an array of format -> [YYYY, MM, DD]
    dateAry = date.split('-')
    # loops through the different part of the array and removes the leading 0's and turns it into an integer
    for i in range(0, len(dateAry)):
        if dateAry[i][0] == "0":
            dateAry[i] = int(dateAry[i][1])
        else:
            dateAry[i] = int(dateAry[i])

    # uses the datetime library to get the day from the date
    d = datetime.datetime(dateAry[0], dateAry[1], dateAry[2])
    dayNum = d.weekday()
    # day = days[dayNum]

    # returnst the day that the date inputed falls on
    return dayNum

print(search('TD40', '08:00', '09:00', '2021-05-03'))
# print(getDay('2021-05-02'))



