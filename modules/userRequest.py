from flask import render_template, request, redirect, session, jsonify
from markupsafe import escape
import random,os,hashlib
from modules.sql import sql


## All functions here will allowed in path for site/user/FUNCTION_NAME
 
## Setup database
if __name__ == "__main__":
    db = sql()
    try:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT NOT NULL,
            isAdmin BOOLEAN DEFAULT 0);
        ''')
    finally:
        db.close()




def encrypt(data):
 return hashlib.sha256("{}WOMBATNET".format(str(data)).encode()).hexdigest()


def register():
    # Guard Clause: Ensure only POST request pass
    if request.method != "POST":
        return {"Success": False, "Message": "Improper method used"}, 405
    with sql() as db:
        if db.execute("SELECT username, password FROM users where username=?", (escape(request.form["Username"]),)).fetchone() == None: # Check if username exists
            db.execute("INSERT INTO users (username, password) VALUES(?,?)", (escape(request.form["Username"]),encrypt(escape(request.form["Password"]))))
            session["Username"] = escape(request.form["Username"])
        else:
            return {"Success": False, "Message": "Ac`count already exist!"}, 401

    return {"Success": True, "Message": "welcome!"}
# Login to user!
def login():

    # Get Method, redirects them
    if request.method == "GET":
        print("Some function used 'GET' on user/login")
        return redirect("/login")

    # Guard Clause: Ensure only POST request pass
    if request.method != "POST":
        return {"Success": False, "Message": "Improper method used"}, 405
     
    # Context Manager: SQL Handler, closes automatically
    with sql() as db:
        userInformation = db.execute("SELECT password, id, isAdmin FROM users where username=?", (escape(request.form["Username"]),)).fetchone() 
        
        ## Account does not exist
        if userInformation == None:
            return {"Success": False, "Message": "Account not registered"}

        if userInformation[0] == encrypt(escape(request.form["Password"])): 
            session["Username"] = escape(request.form["Username"])
            session["UserId"] = userInformation[1]
            if userInformation[2] == 1:
                session["isAdmin"] = True
        else:
            return {"Success": False, "Message": "Invalid credentials"}
            
        return {"Success": True, "Message": "welcome!"}
    
    '''
    db = sql()
    if request.method == "POST":
        if db.execute("SELECT username, password FROM users where username=?", (escape(request.form["Username"]),)).fetchone() == None: # Check if username exists
            db.execute("INSERT INTO users (username, password) VALUES(?,?)", (escape(request.form["Username"]),encrypt(escape(request.form["Password"]))))
            session["Username"] = escape(request.form["Username"])
        else:
            userInformation = db.execute("SELECT password, id, isAdmin FROM users where username=?", (escape(request.form["Username"]),)).fetchone()#[0]
            db.close()
            if userInformation[0] == encrypt(escape(request.form["Password"])): 
                session["Username"] = escape(request.form["Username"])
                session["UserId"] = userInformation[1]
                if userInformation[2] == 1:
                    session["isAdmin"] = True
            else:
                return {"Success": False, "Message": "Invalid credentials"}
            
        return {"Success": True, "Message": "welcome!"}
    
    # Get Method, redirects them
    return redirect("/login")'''

# Get CurrentUser
def currentUser():
    ## Guard Clause: Check for only GET requests
    if request.method != "GET":
       return {"Success": False, "Message": "Improper method used"}, 405
    
    if session.get("Username", None):
        return {"Success": True, "Username": session["Username"], "UserId": session["UserId"]}
    return {"Success": False, "Message": "Not logged in!"}