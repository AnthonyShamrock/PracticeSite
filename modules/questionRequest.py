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
         FOREIGN KEY (category) REFERENCES categories(name)
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
            selectedQuestion = db.execute("SELECT id,question FROM questions WHERE id = ?", (escape(request.args.get("id")),))
        else:
            getQuestions = db.execute("SELECT id,question FROM questions").fetchall()
            selectedQuestion = getQuestions[random.randint(0, len(getQuestions)-1)]
    
    return {"id": selectedQuestion[0], "question": selectedQuestion[1]}

# Add question
def add(): 
    # Guard Clause: Prevent unauthorized methods to pass
    if request.method != "POST":
       return {"Success": False, "Message": "Improper method used"}, 400
    
    # Context Manager: automatically close DB connection after
    with sql() as db:
        try:
            db.execute("INSERT INTO questions (question, answer, category) VALUES (?,?,?)", (escape(request.form["question"]), escape(request.form["answer"]), escape(request.form["category"])))
            return {"Success": True, "Message": "Question added"}
        except:
            return {"Success": False, "Message": "Error Occured"}, 400
    