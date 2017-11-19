from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello Capitole du Libre! We built!"

app.run(host='0.0.0.0')
