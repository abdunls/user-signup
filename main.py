from flask import Flask, request, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

page_header = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-5" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Validation Example</title>
    <link rel="stylesheet" href="/static/app.css" />
  </head>
  <body>
"""

welcomeMessage = """
<h1>SignUp</h1>
 """

form = """
<!doctype html>
<html>
    <body>

        <form action="/signup" id="form" method="POST">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" value="{0}" required>
            <p class="error">{1}</p>
            
            <br></br>

            <label for="password">Password</label>
            <input type="password" name="password" id="password" value="{2}" required>
            <p class="error">{3}</p>
            
            <br></br>

            <label for="password">Verify Password</label>
            <input type="password" name="password2" id="password2" value="{4}" required>
            <p class="error">{5}</p>
            
            <br></br>

            <label for="email">Email (optional)</label>
            <input type="text" name="email" id="email" value="{6}" />
            <p class="error">{7}</p>
            
            <br></br>

            <button type="submit">Submit</button>
        </form>
            
    </body>
</html>
"""

page_footer = """
 </body>
</html>
"""

@app.route("/", methods=["POST", "GET"])
def index():
    # build the response string
    content = page_header + welcomeMessage + form + page_footer
    return render_template("register.html")

@app.route("/signup", methods=["POST"])
def register():
    print("Made it here")
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    password2 = cgi.escape(request.form['password2'])
    email = cgi.escape(request.form['email'])

    usernameError =""
    passwordError = ""
    password2Error ="" 
    emailError = ""

    if not username:
        print("no username")
        usernameError = "Username is required"

    if not password:
        passwordError = "Password is required"
    elif len(password) < 3 or len(password) > 20: 
        passwordError = "Password must be between 3 and 20 characters long"
    else:
        hasSpace = True
        for char in password:
            if char.isspace():
                hasSpace = True
                passwordError = "Password cannot have space"

    if not password2:
        print("no password2")
        password2error = "Please verify password"
    if password  != password2:
        password2Error = "Verify Password must match Password" 

    if email: 
        has_atSign = False
        has_period = False
        for char in email:
            if char == "@": 
                has_atSign = True

            if char == ".":
                has_period = True

        if  not has_atSign:
            emailError = "Email must contain @"
        elif not has_period:
            emailError = "Email must contain ."

        if len(email) < 3 or len(email) > 20: 
            emailError = "Email must be between 3 and 20 characters long" 
        else:
            hasSpace = True
            for char in email:
                if char.isspace():
                    hasSpace = True
                    emailError = "Email cannot have space"
    
    if usernameError or passwordError or password2Error or emailError:
        print("there was an error!")
        content = page_header + form.format(username, usernameError, 
        password, passwordError, password2, password2Error, email, emailError )
        return content 


    return "Welcome, " + username + "!"


# @app.route("/signup", methods=["GET"])
# def register_page():
#     content = page_header + form.format("", "", "", "", "", "") + page_footer
#     return content


@app.route("/form-inputs", methods=["POST"])
def register_page():
    username = request.form['username']
    return "Welcome, " + username + "!"

app.run()