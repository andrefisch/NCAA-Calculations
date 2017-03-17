from flask import Flask, render_template
import pandas
import operator

app = Flask(__name__)

@app.route('/')
def home():
    # name in quotes must be inside templates folder
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/display/')
def display():
    # Get the information and make the dictionary
    html = pandas.read_html("http://escrimeresults.com/NCAA/ncaa2016.html")
    # Create bouts remain dictionary
    boutsRemain = {}
    # go through list of schools at bottom of page
    for i in range(1, len(html[18])):
        schoolColumn = 2
        totalColumn = 3
        remainColumn = 4
        temp = html[18].iloc[i, schoolColumn].strip('\n')
        if (temp in boutsRemain.keys()):
            boutsRemain[temp] = [boutsRemain[temp][0], boutsRemain[temp][1] + otherFencers]
        else:
            boutsRemain[temp] = [html[18].iloc[i, totalColumn], html[18].iloc[i, remainColumn]]
    # pass it to function
    return render_template("display.html", boutsRemain=boutsRemain)

if __name__ == "__main__":
    app.run(debug = True)
