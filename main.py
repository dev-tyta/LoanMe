from flask import Flask, render_template, redirect, url_for, request
from models import db, User, ApplicationData
import pickle
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loan_me.db"
db.init_app(app)

# Load Pickle Files
with open('voting_ensemble.pickle', 'rb') as voting_pickle:
    voting_clf = pickle.load(voting_pickle)

@app.route("/page", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        # Extract and validate form data
        gender = request.form.get("gender")
        married = request.form.get("married")
        dependent = request.form.get("dependent")
        self_employed = request.form.get("self_employed")
        educated = request.form.get("education")
        income = float(request.form.get("income", 0))
        co_income = float(request.form.get("co_income", 0))
        loan_amount = float(request.form.get("loan_amount", 0))
        loan_term = int(request.form.get("loan_term", 0))
        prop = request.form.get("property")

        # Add data validation here (omitted for brevity)

        # Save to database
        application = ApplicationData(gender=gender, married=married, dependent=dependent,
                                      self_employed=self_employed, educated=educated,
                                      income=income, co_income=co_income, loan_amount=loan_amount,
                                      loan_term=loan_term, prop=prop)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("results"))
    return render_template("page.html")

@app.route("/results")
def results():
    latest_application = ApplicationData.query.order_by(ApplicationData.id.desc()).first()
    if latest_application:
        # Prepare the data for prediction
        pred_arr = [latest_application.gender, latest_application.married, latest_application.dependent,
                    latest_application.self_employed, latest_application.educated, latest_application.income,
                    latest_application.co_income, latest_application.loan_amount, latest_application.loan_term,
                    latest_application.prop]
        pred_arr = np.array(pred_arr).reshape(1, -1)
        prediction = voting_clf.predict(pred_arr)
        prediction = round(float(prediction), 2)

        # Render results
        if prediction == 0:
            return render_template("failed.html")
        else:
            return render_template("results.html", prediction=prediction)
    else:
        return "No application data found"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for("homepage"))  # Define 'homepage' route
        else:
            return "Invalid login credentials"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('full-name')
        username = request.form.get('username')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)

        user = User(name=name, username=username, email=email, telephone=telephone, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))  # Redirect to login after signup
    return render_template("signup.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
