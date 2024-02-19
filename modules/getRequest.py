from flask import render_template, request, redirect, session
from markupsafe import escape
import random,os

## All functions here will allowed in path for site/get/FUNCTION_NAME

# Get random question or question via ID

def question():
    request.args.get("id")

    # Check if json, possible id?
    if request.args.get("id") != None:
        sql.select
        cursor.execute("SELECT id,question FROM questions WHERE id = ?", (escape(request.args.get("id")),))
    else:
        cursor.execute("SELECT id,question FROM questions")
    
    getQuestions = cursor.fetchall()
    selectedQuestion = getQuestions[random.randint(0, len(getQuestions)-1)]
    connection.close()
    return {"id": selectedQuestion[0], "question": selectedQuestion[1]}