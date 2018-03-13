from flask import Flask, render_template
from flask_caching import Cache
from requests.adapters import HTTPAdapter
import random
import src.results_sevice as ResultService


app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=300)
def home():
    ranking = ResultService.get_current_results()
    colors = ResultService.get_school_colors()
    return render_template("home.html", ranking=ranking, color=colors[ranking.first_place.name])


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
