from requests.adapters import HTTPAdapter
from flask import Flask, render_template
import random

import src.results_sevice as ResultService


app = Flask(__name__)


@app.route('/')
def home():
    ranking = ResultService.get_current_results()
    return render_template("home.html", ranking=ranking)

@app.route('/about/')
def about():
    # Import list of Andrew quips
    andrewList = []
    with open("./static/text/andrewList.txt") as f:
        for line in f:
            andrewList.append(line.strip('\n'))
    # Import list of Elijah quips
    elijahList = []
    with open("./static/text/elijahList.txt") as f:
        for line in f:
            elijahList.append(line.strip('\n'))

    andrew = random.choice(andrewList)
    elijah = random.choice(elijahList)
    return render_template("about.html", andrew=andrew, elijah=elijah)


if __name__ == "__main__":
    app.run(debug = True)
