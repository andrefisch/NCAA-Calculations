from flask import Flask, render_template
import pandas
import operator
# import os

app = Flask(__name__)

# Import the dictionary file
schoolConversion = {}
# dir = os.path.dirname(os.path.realpath('__file__'))
# filename = dir + "/static/text/schoolDict.txt"
with open("./static/text/schoolDict.txt") as f:
    for line in f:
       (key, val) = line.strip('\n').split(";")
       schoolConversion[key] = val

@app.route('/')
def home():
    # Get the information and make the dictionary
    # 2016 final version
    html = pandas.read_html("http://escrimeresults.com/NCAA/ncaa2016.html")
    # ARCHIVED VERSION WORKS
    # html = pandas.read_html("http://web.archive.org/web/20160325002832/http://www.escrimeresults.com/NCAA/NCAA2016.html")
    # EMPTY DOESNT WORK
    # html = pandas.read_html("http://web.archive.org/web/20160324121938/http://www.escrimeresults.com/NCAA/NCAA2016.html")
    # Create bouts remain dictionary
    boutsRemain = {}
    # go through list of schools at bottom of page
    if (len(html[-2]) > 2):
        for i in range(1, len(html[-2])):
            schoolColumn = 2
            totalColumn = 3
            remainColumn = 4
            temp = html[-2].iloc[i, schoolColumn].strip('\n')
            # 0: total wins
            # 1: bouts remaining
            # 2: bouts to clinch/bouts behind
            # 3: % of bouts needed to clinch/catch leader
            boutsRemain[temp] = [int(html[-2].iloc[i, totalColumn]), int(html[-2].iloc[i, remainColumn]), 0, 0.0, ""]
        # ADD A LITTLE FAKE DATA FOR TESTING
        # {{{
        # boutsRemain["Columbia/Barnard"][0] = 163
        # boutsRemain["Ohio State University"][1] = 10
        # boutsRemain["Princeton University"][1] = 20
        # boutsRemain["St. John's University"][1] = 14
        # boutsRemain["Notre Dame"][1] = 20
        # boutsRemain["Lawrence University"][1] = 200
        # }}}
        # sort the bouts and store information in an array
        schools = len(boutsRemain)
        boutsRemain = sorted(boutsRemain.items(), key=lambda i: i[1][0], reverse=True)
        # make sure references to image files are part of array
        # boutsRemain[0][1][4] = schoolConversion[boutsRemain[0][0]] + ".png"
        for i in range (0, schools):
            # make sure references to image files are part of array
            boutsRemain[i][1][4] = schoolConversion[boutsRemain[i][0]] + ".png"
        # find win differences in wins for teams and fill out array information 
        isOver = True
        for i in range (1, schools):
            # if the difference is greater than all other schools' remaining bouts to fence then it is over
            diff = int(boutsRemain[0][1][0]) - int(boutsRemain[i][1][0])
            if (diff < int(boutsRemain[i][1][1])):
                isOver = False
                # bouts needed to clinch for top school becomes ith place's win total + ith place's remaining bouts - 1st place total bouts
                need = 1 + int(boutsRemain[i][1][0]) + int(boutsRemain[i][1][1]) - int(boutsRemain[0][1][0])
                remain = int(boutsRemain[0][1][1])
                if (remain > 0):
                    boutsRemain[0][1][2] = need
                    boutsRemain[0][1][3] = str(round(need / remain * 100.0, 1)) + "%"
                else:
                    boutsRemain[0][1][2] = "DONE"
                    boutsRemain[0][1][3] = "DONE"
                break
        if (isOver):
            boutsRemain[0][1][2] = "WINNER OF THE 2017"
            boutsRemain[0][1][3] = "NCAA FENCING CHAMPIONSHIP!!"
        for i in range (1, schools):
            # win difference
            diff = int(boutsRemain[0][1][0]) - int(boutsRemain[i][1][0])
            # 
            iRemain = int(boutsRemain[i][1][1])
            firstNeed = 1 + (int(boutsRemain[i][1][1]) + int(boutsRemain[i][1][0])) - int(boutsRemain[0][1][0])
            firstRemain = int(boutsRemain[0][1][1])
            # firstPercent = firstNeed / firstRemain * 100.0
            if (diff > int(boutsRemain[i][1][1])):
                boutsRemain[i][1][2] = diff
                boutsRemain[i][1][3] = "OUT"
            else:
                if (iRemain > 0):
                    iPercent = round(diff / iRemain * 100.0, 1)
                    boutsRemain[i][1][2] = diff
                    boutsRemain[i][1][3] = str(iPercent) + "%"
                else:
                    boutsRemain[i][1][2] = diff
                    boutsRemain[i][1][3] = "OUT"
        # for i in range(0, schools):
            # if (int(boutsRemain[i][1][1]) == 0):
                # boutsRemain[i][1][1] == "DONE"
                # print ("Changed bouts remain for " + boutsRemain[i][0] + " to " + str(boutsRemain[i][1][1]))
    else:

        print ("derp...")
    # name in quotes must be inside templates folder
    return render_template("home.html", boutsRemain=boutsRemain)

@app.route('/about/')
def about():
    return render_template("about.html")

# @app.route('/display/')
# def display():

if __name__ == "__main__":
    app.run(debug = True)
