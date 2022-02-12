from flask import Flask, render_template

# App Config 
app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def hello():
  #return "My name is Manpreet!"
  return render_template('pages/index.html')

if __name__ == "__main__":
  app.run()