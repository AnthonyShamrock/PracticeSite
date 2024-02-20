from flask import render_template, request, redirect, session
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
         isAdmin BOOL DEFAULT 0);
        ''')
    finally:
        db.close()




def encrypt(data):
 return hashlib.sha256("{}WOMBATNET".format(str(data)).encode()).hexdigest()


# Login to user!
def login():
    db = sql()
    
    if request.method == "POST":
        if db.execute("SELECT username, password FROM users where username=?", (escape(request.form["Username"]),)).fetchone() == None:
            db.execute("INSERT INTO users (username, password) VALUES(?,?)", (escape(request.form["Username"]),encrypt(escape(request.form["Password"]))))
            session["Username"] = escape(request.form["Username"])
        else:
            password = db.execute("SELECT password FROM users where username=?", (escape(request.form["Username"]),)).fetchone()[0]
            if password == encrypt(escape(request.form["Password"])): 
                session["Username"] = escape(request.form["Username"])
            else:
                return {"Success": False, "Message": "Invalid credentials"}
        return {"Success": True, "Message": "welcome!"}
    
    # Get Method, redirects them
    return redirect("/login")

def currentUser():
    if request.method == "POST":
       return {"Success": False, "Message": "Improper method used"}
    if session.get("Username", None):
        return {"Success": True, "Username": session["Username"]}
    return {"Success": False, "Message": "Not logged in!"}