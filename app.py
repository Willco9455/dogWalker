''' Imports that will be used throughout the app:
    1. Flask - Flask is the object that creates the flask app and allows all the flask features to be used
    2. render_template - this import is used to allow HTML templates to be used 
    3. request = this import is used when paths are fist loaded to tell which method was used in loading the page
    4. url_for = this is a flask term that is used to create urls that reference files/functions within the app
'''
from flask import Flask, render_template, request, url_for, redirect, session
from database import *
from validation import *
from user import *
from search import *
from datetime import date as d

app = Flask(__name__)        ## Sets the app 
db = dbClass()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

## This says that the function below will be run when the path "website/" is active the methods array is just flask 
## terminology that allows both different mehods to be used in that path(GET and POST)
@app.route('/', methods=['GET', 'POST'])  
def route():
    try:
        savedId = session['usrId']
        return redirect(url_for('home'))
    except:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():   
    ## this will run when the submit button has been pressed becuase that makes the request method POST not GET
    if request.method == "POST":  

        email = request.form["email"] ## sets usr variable to the value that was in the username field
        pas = request.form["pas"] ## sets pas variable to the value that was in the password field

        ## this if statment will run if the login details are incorrect(usrAuth returns false) 
        if not usrAuth(email, pas):
            errorMsg = "Username or Password Incorect"  ## The error message that will be passed back into the template
            return render_template("login.html", error=errorMsg) ## reloaded login template with error message
        
        # This part will get all the details on the user just logged in and saves there unique usrId
        db = dbClass() #Initialised the database 
        usrDetails = (db.search('email', email))[0]
        session['usrId'] = usrDetails[0]

        ## this returns a temporary html page to display to test if the new functionality works
        return redirect(url_for('home'))
    ## This will run when first entereing the webpage 
    else: 
        return render_template('login.html')   ## Whats returned from the function is displayed on the browser so 
                                               ## LOGIN SCREEN will be displayed

## This is the function that will run when the website/register route is loaded 
# It has both get and post becuase post method is used when the user clicks the submit button so the function can
# act differently 
@app.route('/register', methods=['GET', 'POST'])
def register():
    ## When the user has clicked the submit button this if statment runs
    if request.method == "POST": 
        ## The data inputed by the user is taken from the form variables and transfered to python variables with
        # the same name 
        email = request.form['email']
        pas1 = request.form['pas1']
        pas2 = request.form['pas2']
        fName = request.form['fName']
        lName = request.form['lName']
        post = request.form['post'].strip()
        accType = request.form['accType']

        result, err = registerAuth(email, pas1, pas2, post)
        # If statment that checks if the inputed data is valid 
        if result:
            # If the data is valid the new user is added to the datbase using the databases functions
            db.addUsr(email, pas1, fName, lName, accType, post)
            # Then redirects to the login screen 
            return redirect(url_for('login'))
        else:
            ## If the entered details are invalid then redirect back to the register template with the error message
            return render_template('register.html', error=err)

    else:
        ## If the user has not clicked the submit button load the register.html tempalte with no error message
        return render_template('register.html')

@app.route('/home')
def home():
    usrObj = user(session['usrId'])
    return render_template('home.html', usrObj=usrObj)

@app.route('/availability')
def availability():
    # creates a user object for the usre currently logged in
    usrObj = user(session['usrId'])
    # array of the different days that will be looped through within the template 
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # gets the availabilty array for the user currently logged in   
    avail = usrObj.getAvail()
    # this route will render the availability.html tempalte and will have access to the days array within it
    return render_template('availability.html', avail=avail, days=days)


@app.route('/editAvail/<day>', methods=['GET', 'POST'])
def editAvail(day):
    # Once the edit button on the html form has been pressed run this
    if request.method == "POST":
        # creates the user object for the user logged in 
        usrObj = user(session['usrId'])

        ## First try to get the data from the updating time form but if that fails it means that the user has 
        # clicked the not availabile button and so the except code will run if that happens  
        try:
            # If the user has filled in the edit time form then 
            # Gets the variables from the html form that the user entered
            startTime = request.form['startTime']
            endTime = request.form['endTime']

            # checks if the time range entered is valid 
            if not (timeVal(startTime, endTime)):
                err = 'The time range you entered was not valid'
                return render_template('editAvail.html', day=day, err=err)
            # uses the addAvail mehod for the user to add the entered availability into the database
            usrObj.addAvail(day, str(startTime), str(endTime))
        except:
            # If the user has clicked the not availabile button
            request.form['notAvail']
            usrObj.delAvai(day)
        # Redirect back to the availability page
        return redirect(url_for('availability'))
    # Before the button is pressed just render the template
    else:
        return render_template('editAvail.html', day=day)


@app.route('/search', methods=['GET', 'POST'])
def srchRoute():
    # If statment runs after the search button is clicked on the search page
    if request.method == 'POST':
        # Gets all the variables from the form and saves them 
        post = request.form['post'].strip().upper()
        date = request.form['date']
        day = getDay(date)
        startTime = request.form['startTime']
        endTime = request.form['endTime']

        # uses the timeVal from the validation file to check if the start and end times are valid
        if not (timeVal(startTime, endTime)):
            err = 'You have entered an invalid time range for your walk'
            return render_template('search.html', today=d.today(), err=err)

        # Uses the poscodeVal function that returns False if the post code is invalid
        elif not (postcodeVal(post)):
            err = 'The post code you entered is not valid'
            return render_template('search.html', today=d.today(), err=err)

        # saves booking infromation to a session variable called bookingData
        session['bookingData'] = [session['usrId'], date, day, startTime, endTime]

        # uses the search fucntion already created to get all walkers avaialbe for walking
        available = search(post, date, startTime, endTime)

        # loades the results template and passess in the array of avaiabel users so that data can be 
        # used within the template 
        return render_template('results.html', available=available, startTime=startTime, endTime=endTime)
    # else runs for when the /search route is navigated to normaly not POST method
    else:
        return render_template('search.html', today=d.today())


@app.route('/confirm/<walkerId>', methods=['GET', 'POST'])
def confirm(walkerId):
    # creates a user object for the walker that the booking is going to be 
    # for, will be passed into the html template 
    walker = user(walkerId)
    # Gets the booking data in the format -->
    # [ownerId,date,day,startTime,endTime]
    bookingData = session['bookingData']

    # If statment that runs when the confirm button is pressed
    if request.method == 'POST':
        # Adds the booking to the booking table 
        db.addBooking(bookingData[0], walker.usrId, bookingData[1], bookingData[2], bookingData[3], bookingData[4])
        # Takes the user badck to the hoem screen
        return redirect(url_for('home'))
    else:
        # Renderes the confim.html page
        return render_template('confirm.html', walker=walker, bookingData=session['bookingData'])
 
# Takes in the accType as a varible from the path used to get to the file  
@app.route('/bookings/<accType>')
def bookings(accType):
    # If the acount type is owner than use the getownerbooking method
    # else use getwalkerbooking method
    if accType == 'Owner':
        bookings = db.getOwnerBookings(session['usrId'])
        return render_template('bookings.html', bookings=bookings, user=user, accType=accType)
    else:
        bookings = db.getWalkerBookings(session['usrId'])
        return render_template('bookings.html', bookings=bookings, user=user, accType=accType)


@app.route('/profile/<usrId>')
def profile(usrId):
    userObj = user(usrId)
    return render_template('profile.html', userObj=userObj, user=user)


@app.route('/leaveReview/<forId>', methods=['GET', 'POST'])
def leaveReview(forId):
    if request.method == 'POST':
        db.makeReview(session['usrId'], forId, d.today(), int(request.form['star']), request.form['message'])
        return redirect(f'/profile/{forId}')
    else: 
        return render_template('leaveReview.html')

if __name__ == '__main__':  ## This makes sure the app runs when the python file is ran 
    app.run(debug = True)   ## The debug = true turns the debug on so that when there is an syntax error the 
                            ## browser will show where the problem is, making debugging eaiser


    
