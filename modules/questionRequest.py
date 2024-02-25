from flask import render_template, request, redirect, session
from markupsafe import escape
import random
from modules.sql import sql 

## All functions here will allowed in path for site/question/FUNCTION_NAME

## Setup database
with sql() as db:
    #DB: Categories
    db.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')
    
    #DB: questions
    db.execute('''CREATE TABLE IF NOT EXISTS questions (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         question TEXT UNIQUE,
         answer TEXT NOT NULL,
         category TEXT NOT NULL,
         addedBy INTEGER NOT NULL,
         FOREIGN KEY (category) REFERENCES categories(name),
         FOREIGN KEY (addedBy) REFERENCES users(id)
        )''')

# Get random question or question via ID
def get():
    # Guard Clause: Prevent unauthorized methods to pass
    if request.method != "GET":
        return {"Success": False, "Message": "Improper method used"}, 400

   # Context Manager: automatically close DB connection after
    with sql() as db:
        selectedQuestion = None  # Used question Information 

        # Request have questionId included? 
        if request.args.get("id") != None:
            selectedQuestion = db.execute("SELECT id,question,category,addedBy FROM questions WHERE id = ?", (escape(request.args.get("id")),))
        else:
            getQuestions = db.execute("SELECT id,question,category,addedBy FROM questions").fetchall()
            selectedQuestion = getQuestions[random.randint(0, len(getQuestions)-1)]
            print(selectedQuestion)
    
    return {"id": selectedQuestion[0], "question": selectedQuestion[1], "Category": selectedQuestion[2]}

# Add question
def add(): 
    # Guard Clause: Prevent unauthorized methods to pass
    if request.method != "POST":
       return {"Success": False, "Message": "Improper method used"}, 400
    
    ## Ensure user is logged in!
    if session == {}:
        return {"Success": False, "Message": "User not logged in!"}, 401
    
    # Context Manager: automatically close DB connection after
    with sql() as db:
        try:
            print(session)
            db.execute("INSERT INTO questions (question, answer, category, addedBy) VALUES (?,?,?,?)", (escape(request.form["question"]), escape(request.form["answer"]), escape(request.form["category"]), int(session["UserId"])))
            return {"Success": True, "Message": "Question added"}
        except:
            return {"Success": False, "Message": "Error occured"}, 500
    
# Get Categories
def categories():
     # Guard Clause: Prevent unauthorized methods to pass
    if request.method != "GET":
       return {"Success": False, "Message": "Improper method used"}, 400
   
    # Context Manager: automatically close DB connection after
    with sql() as db:
        try:
            returnTable = []
            for category in db.execute("SELECT name FROM categories").fetchall():
                returnTable.append(category[0])
            return {"Success": True, "Categories": returnTable}
        except:
            return {"Success": False, "Message": "Error Occured"}, 400