from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail


with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = params["local_server"]

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_id'],
    MAIL_PASSWORD = params['gmail_pssd']
)

mail = Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_num = db.Column(db.String, nullable=False)
    msg = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)


@app.route("/")
def home():
    return render_template("index.html", params = params)

@app.route("/about")
def about():
    return render_template("about.html", params = params)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        #Retriving data from website
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        
        # Entring date to database
        entry = Contact(name=name, phone_num = phone, msg = message, date = datetime.now(), email = email)

        db.session.add(entry)
        db.session.commit()

        # Sending Mail
        print(email)
        mail.send_message('New message from ' + name,
                          sender = email,
                          recipients = [params['gmail_id']],
                          body = message + "\n" + phone
                          )

    return render_template("contact.html", params = params)

@app.route("/post")
def post():
    return render_template("post.html", params = params)

app.run(debug=True)
