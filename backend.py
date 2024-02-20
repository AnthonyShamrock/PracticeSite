## CONSTANTS (UPPER_SNAKE_CASE)
ALLOWED_GET_REQUEST_PATHS=[] # This autopopulate based off the module getRequest
ALLOWED_USER_REQUEST_PATHS=[] # This autopopulate based off the module userRequest


## Packages
from inspect import isfunction, getmodule # Used to get functions for APIs
from flask import Flask, render_template, request, redirect, session
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
import os


## Modules
import modules.getRequest as getRequest
import modules.userRequest as userRequest
import modules.sql as sql

## Start app
app = Flask(__name__)
app.secret_key = "wombat.netTESTING" ## For sessions
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Get functions (exclude packages) from module
def getFunctionsFromModule(module):
    return [func.__name__ for func in module.__dict__.values() if isfunction(func) and getmodule(func) == module]

'''
GET REQUEST
type: {categories | question}
id: {type: question?}
'''

# populates ALLOWED_GET_REQUEST_PATHS with function names
ALLOWED_GET_REQUEST_PATHS = getFunctionsFromModule(getRequest)

@app.route('/get/<string:requestType>', methods=['GET']) ## Make request data send over URL with URL
def get(requestType=None):
  # Guard Clause: Ensure request has requestType
  if not requestType:
       return {"Success": False, "Message": 'Missing requestType'}, 400
  
  # List Validation: Check if requestType is in (CONSTANT) ALLOWED_GET_REQUEST_PATHS
  if not requestType in ALLOWED_GET_REQUEST_PATHS:
      return {"Success": False, "Message": 'invalid requestType'}, 400
  
  # Execute function in getRequest module
  return getattr(getRequest, escape(requestType))()


# populates ALLOWED_USER_REQUEST_PATHS
ALLOWED_USER_REQUEST_PATHS = getFunctionsFromModule(userRequest)

@app.route('/user/<string:requestType>', methods=['GET', 'POST']) ## Make request data send over URL with URL
def user(requestType=None):
  # Guard Clause: Ensure request has requestType
  if not requestType:
       return {"Success": False, "Message": 'Missing requestType'}, 400
  
  # List Validation: Check if requestType is in (CONSTANT) ALLOWED_USER_REQUEST_PATHS
  if not requestType in ALLOWED_USER_REQUEST_PATHS:
      return {"Success": False, "Message": 'invalid requestType'}, 400
  
  # Execute function in getRequest module
  return getattr(userRequest, escape(requestType))()

# MOVING SOON!
@app.route('/submit', methods=['POST'])
def submit_answer():
    if request.content_type != "application/json":
       return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
    connection = None;#sqlite3.connect("website.db")
    cursor = connection.cursor()

    data = request.get_json()
    cursor.execute("SELECT answer FROM questions WHERE id = ?", (data["id"],))
    correctAnswer = cursor.fetchone()[0]
    connection.close()

    if data['answer'] == correctAnswer:
        return "Correct!"
    else:
        return "Incorrect. The correct answer is: " + correctAnswer

# MOVING SOON!
@app.route("/add", methods=['POST'])
def add_question():
    if request.content_type != "application/json":
        return {"Success": False, "Message": 'Content_Type != "application/json"'}, 400
    connection = None;#sqlite3.connect("website.db")

    data = request.get_json()
    connection.execute("INSERT INTO questions (question, answer) VALUES(?, ?)", (data["question"], data["answer"]))
    connection.commit()
    return {"Success": True, "Message": 'Added'}

# Handle serve all static pages! :D
@app.route("/")
@app.route("/<string:pageName>")
def run(pageName=None):
    if pageName and os.path.exists("templates/{}.html".format(escape(pageName))):
        return render_template("{}.html".format(escape(pageName)))
    return render_template("getQuestion.html")

if __name__ == '__main__':
    app.run(port = 3001, use_reloader=False)