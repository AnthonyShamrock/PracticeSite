from flask import Flask, render_template, request
from markupsafe import escape
import sqlite3
import random
import os

app = Flask(__name__)

## SQL initialization
connection = sqlite3.connect("website.db")
cursor = connection.cursor()
connection.commit()

@app.route('/get', methods=['GET'])
def get():
  # SQL
  connection = sqlite3.connect("website.db")
  cursor = connection.cursor()

  # Check if json, possible id?
  if request.content_type == "application/json":
    data = request.get_json()
    cursor.execute("SELECT id,question FROM questions WHERE id = ?", (data["id"],))
  else:
    cursor.execute("SELECT id,question FROM questions") # Random question

  getQuestions = cursor.fetchall()
  selectedQuestion = getQuestions[random.randint(0, len(getQuestions)-1)]
  connection.close()
  return {"id": selectedQuestion[0], "question": selectedQuestion[1]}

@app.route('/submit', methods=['POST'])
def submit_answer():
    if request.content_type != "application/json":
       return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
    connection = sqlite3.connect("website.db")
    cursor = connection.cursor()

    data = request.get_json()
    cursor.execute("SELECT answer FROM questions WHERE id = ?", (data["id"],))
    correctAnswer = cursor.fetchone()[0]
    connection.close()

    if data['answer'] == correctAnswer:
        return "Correct!"
    else:
        return "Incorrect. The correct answer is: " + correctAnswer

@app.route("/add", methods=['POST'])
def add_question():
    if request.content_type != "application/json":
        return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
    connection = sqlite3.connect("website.db")

    data = request.get_json()
    connection.execute("INSERT INTO questions (question, answer) VALUES(?, ?)", (data["question"], data["answer"]))
    connection.commit()
    return {"Success": True, "Message": 'Added'}


@app.route("/isDeveloper", methods=['POST'])
def isDeveloper():
   if request.content_type != "application/json":
        print(request.content_type)
        return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
   
   data = request.get_json()
   if data["secret"] == "wombat":
      return {"Success": True, "Message": 'User is Developer', "Key": str(random.random())}
   
   return {"Success": False, "Message": 'Unauthorized User'}, 401

@app.route("/")
@app.route("/<pageName>")
def run(pageName=None):
    if pageName and os.path.exists("templates/{}.html".format(escape(pageName))):
        return render_template("{}.html".format(escape(pageName)))
    return render_template("getQuestion.html")

if __name__ == '__main__':
    app.run(port = 3001)