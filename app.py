from flask import Flask, render_template      ## Imports that will be used throughout the app 
app = Flask(__name__)        ## Sets the app 

@app.route('/')              ## This says that the function below will be run when the path "website/" is active
def logIn():                 
    return render_template("login.html")    ## Whats returned from the function is displayed on the browser so LOGIN SCREEN 
                                      ## will be displayed

if __name__ == '__main__':  ## This makes sure the app runs when the python file is ran 
    app.run(debug = True)   ## The debug = true turns the debug on so that when there is an syntax error the 
                            ## browser will show where the problem is, making debugging eaiser