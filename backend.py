from flask import Flask, render_template, request, jsonify
#from flask_restful import Resource, Api

app = Flask(__name__)
#api = Api(app)

# Mock database with questions and answers
questions = {
    1: {"question": "What is 2 + 2?", "answer": "4"},
    2: {"question": "What is the capital of France?", "answer": "Paris"},
    3: {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
}

@app.route('/get', methods=['GET'])
def get():
  question_id = request.args.get('id') or 1
  return jsonify(questions[question_id])

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