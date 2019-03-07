from flask import Flask, render_template
from flask_caching import Cache
from requests.adapters import HTTPAdapter
import random
import src.results_sevice as ResultService


app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

default = "Default"

@app.route('/')
@cache.cached(timeout=150)
def home():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
        ranking, fencers, weapons = ResultService.get_current_results()
        return render_template("home.html", ranking=ranking, color=colors[ranking.first_place.name], year=year)
    except:
        print("Error loading HOME page")
        schools = ResultService.get_fencer_numbers()
        return render_template("display.html", schools=schools, year=year, color=colors[default])

@app.route('/individual/')
@cache.cached(timeout=150)
def individual():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
        ranking, fencers, weapons = ResultService.get_current_results()
        return render_template("individual.html", fencers=fencers, weapons=weapons, color=colors[ranking.first_place.name], year=year)
    except:
        print("Error loading INDIVIDUAL page")
        schools = ResultService.get_fencer_numbers()
        return render_template("display.html", schools=schools, year=year, color=colors[default])

@app.route('/about/')
def about():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
        # ranking, fencers, weapons = ResultService.get_current_results()
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
        # return render_template("about.html", andrew=andrew, elijah=elijah)
        return render_template("about.html", color=colors[default], year=year, andrew=andrew, elijah=elijah)
    except:
        print("Error loading ABOUT page")
        schools = ResultService.get_fencer_numbers()
        return render_template("display.html", schools=schools, year=year, color=colors[default])

@app.route('/moneyball/')
def moneyball():
    colors = ResultService.get_school_colors()
    try:
        ranking, fencers, weapons = ResultService.get_current_results()
        return render_template("moneyball.html", fencers=fencers, weapons=weapons, color=colors[ranking.first_place.name])
    except:
        schools = resultservice.get_fencer_numbers()
        return render_template("display.html", schools=schools, color=colors[default])


if __name__ == "__main__":
    app.run(debug = True)
