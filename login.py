from database import dbClass
db = dbClass()

## Takes input of a username and password and will return true if they are valid and false if not. Used for the 
# login page
def usrAuth(email, pas):
     
     ## This try and except will try to retive the record for the username entered and store it in dbUser however 
     # if no username exists(result of search function returns empyt) the whole function will return false
    try:
        dbUser = (db.search('email', email))[0]
        print(dbUser)
    except:
        print('couldent search')
        return False

    ## correct details, that are fetched from the server
    corrEmail = dbUser[1]
    corrPas = dbUser[2]

    ## return true if they are valid and false if not
    if corrEmail == email and corrPas == pas:
        return True
    else: 
        return False

## Function for register screen that verifies that all the details entered into the form are valid 
def registerAuth(email, pas1, pas2):
    ## This section will check if the username is already taken or not 
    reslt = db.search('email', email)
    if len(reslt) > 0: 
        err = 'That email already has an account'
        return False, err

    ## First part checks if the username is grater than or equal to 8 characters
    if not('@' in email):
        err = 'That is not a valid email address'
        return False, err

    ## Checks if passwords match
    if pas1 != pas2:
        ## error message that will apear on the register screen 
        err = 'Passwords do not match'
        return False, err
    
    # Checks if the pasword is grater than or equal to 8
    if len(pas1) < 8:
        err = 'Password must be at least 8 characters long'
        return False, err


    ## This verifies if the password has at least 1 number in it
    val = False # Variable that will change to True if number found
    for i in pas1: # Loops through each charater in the password
        # If the charcter is a number set val to True 
        if i.isdigit():
            val = True
    # If val is False exit the function and return False
    if not val:
        err  = 'Password does not include any numbers'
        return False, err


    ## This section happens when all register criteria are fit
    print('valid') ## temporaty for testing purposes 
    return True, '' 
    
#           username  password1  password2
# registerAuth('Username', 'Password', 'Password1')

