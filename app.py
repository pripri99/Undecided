from flask import Flask

# App Config 
app = Flask(__name__)

@app.route("/")
def hello():
  return "My name is Manpreet!"

if __name__ == "__main__":
  app.run()