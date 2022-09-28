from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loan_me.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user = db.Column(db.String(50))
    email = db.Column(db.String(150))
    telephone = db.Column(db.Integer(20))
    password = db.Column(db.String(70))

    def __repr__(self):
        return "Contact" + str(self.id)


class ApplicationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10))
    married = db.Column(db.String(10))
    dependent = db.Column(db.String(5))
    self_employed = db.Column(db.String(20))
    educated = db.Column(db.String(50))
    income = db.Column(db.Integer)
    co_income = db.Column(db.Integer)
    loan_amount = db.Column(db.Imteger)
    loan_term = db.Column(db.Interger)

    def __repr__(self):
        return "Data" + str(self.id)


voting_pickle = open('voting_ensemble.pickle', 'rb')
map_pickle = open('output_result.pickle', 'rb')

voting_clf = pickle.load(voting_pickle)
unique_mapping = pickle.load(map_pickle)


@app.route("/home")
def homepage():
    return render_template("")


@app.route("/application-page")
def display():

    return render_template("page.html")


@app.route("/application-results")
def results():
    return render_template("results.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == 'post':
        mail = request.form["email"]
        password = request.form["password"]

        log_in = User.query.filter_by(mail=mail, password=password).first()
        if log_in is not None:
            redirect(url_for("homepage"))
    return render_template("login.html")


@app.route("/signup", methods=["get", "post"])
def signup():
    if request.method == "post":
        name = request.form['full-name']
        user = request.form['username']
        mail = request.form['email']
        telephone = request.form['telephone']
        password = request.form['password']

        sign_up = User(name=name, user=user, mail=mail, telephone=telephone, password=password)
        db.session.add(sign_up)
        db.session.commit()
    return render_template("signup.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
