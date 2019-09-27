from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route('/', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    verify_error = ""
    email_error = ""
    validator1 = False
    validator2 = False 

    username_error = isValid(username, "Username")
    if username_error == "":
        username_error = spaceCheck(username, "Username")
    
    password_error = isValid(password, "Password")
    if password_error == "":
        password_error = spaceCheck(password, "Password")

    if (not verify) or (verify.strip() == ""):
            verify_error = "Passwords don't match"    

    if  verify != password:
        verify_error = "Passwords don't match" 
    
    if email != "":  
        for i in email:
            if i =="@":
                validator1 = True
    
    if email != "":
        for i in email:
            if i == ".":
                validator2 = True

    if email != "":
        for i in email:
            if i == " ":
                email_error= "Email is not valid"             

    if email != "":
        if validator1 == False or validator2 == False:
            email_error = "Email is not valid"
    if email != "":
        if len(email) <3 or len(email)>20:
            email_error = "Email is not valid"        

    if username_error == "" and password_error == "" and verify_error == "" and email_error == "" :
      return redirect(f'/welcome?username={username}')
  

    return render_template("sign-up.html", 
        username_error=username_error, password_error=password_error, 
        verify_error=verify_error,email_error=email_error, 
        username=username, email=email, title="User Sign Up")

def isValid(item, name):
    if (not item) or (item.strip() == "") or (len(item) < 3) or (len(item) > 19) :
        return "Not a valid "+name
    else:
        return ""  

def spaceCheck(item, name):
    for i in item:
        if i == " ":
            return "Not a valid "+ name
    return ""    


@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username = username)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('sign-up.html', username="", email="", title="User Sign Up")

app.run()