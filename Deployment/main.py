from flask import Flask, render_template, redirect
import pickle

app = Flask(__name__)

voting_pickle = open('voting_ensemble.pickle', 'rb')
map_pickle = open('output_result.pickle', 'rb')

voting_clf = pickle.load(voting_pickle)
unique_mapping = pickle.load(map_pickle)


@app.route("/availability")
def display():
    return render_template("page.html")
