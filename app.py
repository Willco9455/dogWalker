''' Imports that will be used throughout the app:
    1. Flask - Flask is the object that creates the flask app and allows all the flask features to be used
    2. render_template - this import is used to allow HTML templates to be used 
    3. request = this import is used when paths are fist loaded to tell which method was used in loading the page
    4. url_for = this is a flask term that is used to create urls that reference files/functions within the app
'''
from flask import Flask, render_template, request, url_for, redirect
from database import dbClass
from login import *

app = Flask(__name__)        ## Sets the app 
db = dbClass()

## This says that the function below will be run when the path "website/" is active the methods array is just flask 
## terminology that allows both different mehods to be used in that path(GET and POST)
@app.route('/', methods=['GET', 'POST'])  
def login():       
    ## this will run when the submit button has been pressed becuase that makes the request method POST not GET
    if request.method == "POST":  

        usr = request.form["usr"] ## sets usr variable to the value that was in the username field
        pas = request.form["pas"] ## sets pas variable to the value that was in the password field

        ## this if statment will run if the login details are incorrect(usrAuth returns false) 
        if not usrAuth(usr, pas):
            errorMsg = "Username or Password Incorect"  ## The error message that will be passed back into the template
            return render_template("login.html", error=errorMsg) ## reloaded login template with error message

        ## this returns a temporary html page to display to test if the new functionality works
        return f"""
            <h1>LOGIN SUCCESSFUL</h1><br>
            
            <p>your username is {usr}</p>
            <p>your password is {pas}</p>
        """
    ## This will run when first entereing the webpage 
    else: 
        return render_template('login.html')   ## Whats returned from the function is displayed on the browser so 
                                               ## LOGIN SCREEN will be displayed

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST": 
        usr = request.form['usr']
        pas1 = request.form['pas1']
        pas2 = request.form['pas2']
        if registerAuth(usr, pas1, pas2):
            db.addUsr(usr, pas1)
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='There was an error')

    else:
        return render_template('register.html')



if __name__ == '__main__':  ## This makes sure the app runs when the python file is ran 
    app.run(debug = True)   ## The debug = true turns the debug on so that when there is an syntax error the 
                            ## browser will show where the problem is, making debugging eaiser


    
