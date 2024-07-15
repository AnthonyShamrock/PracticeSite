## CONSTANTS (UPPER_SNAKE_CASE)
ALLOWED_QUESTION_REQUEST_PATHS=[] # This autopopulate based off the module getRequest
ALLOWED_USER_REQUEST_PATHS=[] # This autopopulate based off the module userRequest


## Packages
from inspect import isfunction, getmodule # Used to get functions for APIs
from flask import Flask, render_template, request, redirect, session, current_app, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
import os

## Modules
import modules.questionRequest as questionRequest
import modules.userRequest as userRequest
import modules.sql as sql

## Start app
app = Flask(__name__)
app.secret_key = "wombat.netTESTING" ## For sessions
app.SERVER_NAME = "localhost"
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

# populates ALLOWED_QUESTION_REQUEST_PATHS with function names
ALLOWED_QUESTION_REQUEST_PATHS = getFunctionsFromModule(questionRequest)

@app.route('/question/<string:requestType>', methods=['GET', "POST"]) ## Make request data send over URL with URL
def get(requestType=None):
  # Guard Clause: Ensure request has requestType
  if not requestType:
       return {"Success": False, "Message": 'Missing requestType'}, 400
  
  # List Validation: Check if requestType is in (CONSTANT) ALLOWED_GET_REQUEST_PATHS
  if not requestType in ALLOWED_QUESTION_REQUEST_PATHS:
      return {"Success": False, "Message": 'invalid requestType'}, 400
  
  # Execute function in getRequest module
  return getattr(questionRequest, escape(requestType))()


# populates ALLOWED_USER_REQUEST_PATHS with function names
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

# Handle serve all static pages! :D
@app.route("/")
@app.route("/<string:pageName>")
def run(pageName=None):
    if pageName and os.path.exists("templates/{}.html".format(escape(pageName))):
        return render_template("{}.html".format(escape(pageName)))
    return render_template("getQuestion.html")

if __name__ == '__main__':
    app.permanent_session_lifetime = 21600 # Automatically log off after 6 hours!
    app.run(port = 3001)