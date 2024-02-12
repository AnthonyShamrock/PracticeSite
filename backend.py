from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# Mock database with questions and answers
questions = {
    1: {"question": "What is 2 + 2?", "answer": "4"},
    2: {"question": "What is the capital of France?", "answer": "Paris"},
    3: {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
}

db = pymysql.connect(host="localhost", user="cisco", password="WombatCisco", database="PracticeSite")


@app.route('/get', methods=['GET'])
def get():
  cursor = db.cursor()
  cursor.execute("SELECT 1 FROM Questions")
  return jsonify(cursor.fetchone())

@app.route('/submit', methods=['POST'])
def submit_answer():
    print(request)
    data = request.get_json()
    question_id = data['id']
    user_answer = data['answer']
    correct_answer = questions[int(question_id)]["answer"]
    
    if user_answer == correct_answer:
        return "Correct!"
    else:
        return "Incorrect. The correct answer is: " + correct_answer

@app.route("/")
def init():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port = 3001)
    print("up")