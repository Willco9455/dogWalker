from database import dbClass
db = dbClass()

## Takes input of a username and password and will return true if they are valid and false if not. Used for the 
# login page
def usrAuth(usr, pas):
     
     ## This try and except will try to retive the record for the username entered and store it in dbUser however 
     # if no username exists(result of search function returns empyt) the whole function will return false
    try:
        dbUser = (db.search('username', usr))[0]
    except:
        print('couldent search')
        return False

    ## correct details, that are fetched from the server
    corrUsr = dbUser[1]
    corrPas = dbUser[2]

    ## return true if they are valid and false if not
    if corrUsr == usr and corrPas == pas:
        return True
    else: 
        return False

## Function for register screen that verifies that all the details entered into the form are valid 
def registerAuth(usr, pas1, pas2):
    ## First part checks if the username is grater than or equal to 8 characters
    if len(usr) < 8:
        print('username must be at least 8 characters long')
        return False

    ## Checks if passwords match
    if pas1 != pas2:
        print('passwords do not match')
        return False

    ## This verifies if the username has at least 1 number in it
    val = False # Variable that will change to True if number found
    for i in pas1: # Loops through each charater in the username 
        # If the charcter is a number set val to True 
        if i.isdigit():
            val = True  
    # If val is False exit the function and return False
    if not val:
        print('No Number')
        return False

    # Checks if the pasword is grater than or equal to 8
    if len(pas1) < 8:
        print('Password must be at least 8 characters long')
        return False

    ## This section happens when all register criteria are fit
    print('valid') ## temporaty for testing purposes 
    return True 
    
#           username  password1  password2
registerAuth('Username', 'Password', 'Password1')

