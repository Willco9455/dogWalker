from database import dbClass


db = dbClass()

class user:
    usrId = 0
    email = ""
    pas = ""
    fName = ""
    lName = ""
    accType = ""
    postcode = ""
    starRating = 0
    def __init__(self, usrId):
        # Creates details varibale that holds the record of the user with a inputed usrId 
        details = (db.search('usrId', usrId))[0]
        # Uses the datails fetched from the database and assigns the data to the attributes of the object
        self.usrId = details[0]
        self.email = details[1]
        self.pas = details[2]
        self.fName = details[3]
        self.lName = details[4]
        self.accType = details[5]
        self.postcode = details[6]
        self.starRating = details[8]

    # Method for the user that uses the database getAivail function to get the users availabilty array
    def getAvail(self): 
        avail = db.getAvail(self.usrId)
        return avail

    # Method that users the database function addAvail to add/replace availabilty for a specific day 
    def addAvail(self, day, startTime, endTime):
        db.addAvail(self.usrId, day, startTime, endTime)
    
    def delAvai(self, day):
        db.delAvail(self.usrId, day)

    def getReviewsFor(self):
        result = db.getReviewsFor(self.usrId)
        return result
