from flask import Flask

# App Config 
app = Flask(__name__)

@app.route("/")
def hello():
  return "My name is Kerushani!"
if __name__ == "__main__":
  app.run()