from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/about")
def harshit():
    return render_template("about.html", name="Harshit")
app.run(debug=True)