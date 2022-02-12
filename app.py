from flask import Flask, render_template, request
import json
from AI_response import *

# App Config 
app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def index():
  return render_template('pages/index.html')

@app.route('/speech')
def speech():
    return render_template('pages/speech.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)
    res = answer(jsdata)
    print(res)
    return json.loads(jsdata)[0]

@app.route("/register")
def register():
  return render_template('pages/auth/register.html')

@app.route("/login")
def login():
  return render_template('pages/auth/login.html')

@app.route("/logout")
def logout():
  return "Login out "

if __name__ == "__main__":
  app.run()