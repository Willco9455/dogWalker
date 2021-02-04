''' Imports that will be used throughout the app:
    1. Flask - Flask is the object that creates the flask app and allows all the flask features to be used
    2. render_template - this import is used to allow HTML templates to be used 
    3. request = this import is used when paths are fist loaded to tell which method was used in loading the page
'''
from flask import Flask, render_template, request 
app = Flask(__name__)        ## Sets the app 

## This says that the function below will be run when the path "website/" is active the methods array is just flask 
## terminology that allows both different mehods to be used in that path(GET and POST)
@app.route('/', methods=['GET', 'POST'])  
def login():       
    if request.method == "POST":
        return "<h1>LOGIN SUCCESSFUL<h1>"
    else: 
        return render_template("login.html")   ## Whats returned from the function is displayed on the browser so 
                                               ## LOGIN SCREEN will be displayed

if __name__ == '__main__':  ## This makes sure the app runs when the python file is ran 
    app.run(debug = True)   ## The debug = true turns the debug on so that when there is an syntax error the 
                            ## browser will show where the problem is, making debugging eaiser
