from flask import Flask, render_template, request

# App Config 
app = Flask(__name__)
app.config.from_object('config')



@app.route("/")
def index():
  print(request.endpoint)
  return render_template('pages/home.html')

@app.route("/ask")
def ask():
  print(request.endpoint)
  return render_template('pages/discussion/askMeAnything.html')

@app.route("/community")
def community():
  print(request.endpoint)
  return render_template('pages/discussion/community.html')

@app.route("/conversation")
def conversation():
  print(request.endpoint)
  return render_template('pages/discussion/conversation.html')

@app.route("/register")
def register():
  return render_template('pages/auth/register.html')

@app.route("/login")
def login():
  return render_template('pages/auth/login.html')


@app.route("/logout")
def logout():
  return "Login out"

if __name__ == "__main__":
  app.run()