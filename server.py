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
        weapons = ["Total Fencers", "Men's Epee", "Men's Foil", "Men's Sabre", "Women's Epee", "Women's Foil", "Women's Sabre"]
        schools = ResultService.get_fencer_numbers()
        return render_template("display.html", schools=schools, weapons=weapons, year=year, color=colors[default])

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
        weapons = ["Total Fencers", "Men's Epee", "Men's Foil", "Men's Sabre", "Women's Epee", "Women's Foil", "Women's Sabre"]
        schools = ResultService.get_fencer_numbers()
        return render_template("display.html", schools=schools, weapons=weapons, year=year, color=colors[default])

@app.route('/about/')
def about():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
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
        order = ['men', 'women']
        if (int(year) % 2 == 0):
            order = ['women', 'men']
        return render_template("about.html", color=colors[default], year=year, order=order, andrew=andrew, elijah=elijah)
    except:
        print("Error loading ABOUT page")
        schools = ResultService.get_fencer_numbers()
        weapons = ["Total Fencers", "Men's Epee", "Men's Foil", "Men's Sabre", "Women's Epee", "Women's Foil", "Women's Sabre"]
        return render_template("display.html", schools=schools, weapons=weapons, year=year, color=colors[default])

@app.route('/schedule/')
def schedule():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
        order = ['Men', 'Women']
        if (int(year) % 2 == 0):
            order = ['Women', 'Men']
        return render_template("schedule.html", color=colors[default], year=year, order=order)
    except:
        print("Error loading ABOUT page")
        schools = ResultService.get_fencer_numbers()
        weapons = ["Total Fencers", "Men's Epee", "Men's Foil", "Men's Sabre", "Women's Epee", "Women's Foil", "Women's Sabre"]
        return render_template("display.html", schools=schools, weapons=weapons, year=year, color=colors[default])

@app.route('/moneyball/')
def moneyball():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    try:
        ranking, fencers, weapons = ResultService.get_current_results()
        return render_template("moneyball.html", fencers=fencers, weapons=weapons, color=colors[ranking.first_place.name])
    except:
        schools = resultservice.get_fencer_numbers()
        weapons = ["Total Fencers", "Men's Epee", "Men's Foil", "Men's Sabre", "Women's Epee", "Women's Foil", "Women's Sabre"]
        return render_template("display.html", schools=schools, weapons=weapons, year=year, color=colors[default])


if __name__ == "__main__":
    app.run(debug = True)
