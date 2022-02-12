from flask import Flask, render_template

# App Config 
app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def index():
  return render_template('pages/index.html')

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