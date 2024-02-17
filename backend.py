from flask import Flask, render_template, request, jsonify
from markupsafe import escape
import sqlite3
import random
import os

app = Flask(__name__)

# Mock database with questions and answers
questions = {
    1: {"question": "What is 2 + 2?", "answer": "4"},
    2: {"question": "What is the capital of France?", "answer": "Paris"},
    3: {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
}

connection = sqlite3.connect("website.db")
cursor = connection.cursor()
connection.commit()

@app.route('/get', methods=['GET'])
def get():
  connection = sqlite3.connect("website.db")
  cursor = connection.cursor()
  if request.content_type == "application/json":
    data = request.get_json()
    cursor.execute("SELECT id,question FROM questions WHERE id = ?", (data["id"],))
  else:
    cursor.execute("SELECT id,question FROM questions")
  getQuestions = cursor.fetchall()
  selectedQuestion = getQuestions[random.randint(0, len(getQuestions)-1)]
  connection.close()
  return jsonify({"id": selectedQuestion[0], "question": selectedQuestion[1]})

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
        return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
   
   return {"Success": True, "Message": 'User is Developer'}

@app.route("/")
@app.route("/<pageName>")
def run(pageName=None):
    if pageName and os.path.exists("templates/{}.html".format(escape(pageName))):
        return render_template("{}.html".format(escape(pageName)))
    return render_template("getQuestion.html")

if __name__ == '__main__':
    app.run(port = 3001)