from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

from lxml import html
from flask import Flask, render_template
from io import BytesIO
import requests
import pandas
import operator
import random

app = Flask(__name__)

# Import the dictionary file for school conversion
schoolConversion = {}
with open("./static/text/schoolDict.txt") as f:
    for line in f:
        (key, val) = line.strip('\n').split(";")
        schoolConversion[key] = val
fencersPerSchool = {}
# Import the dictionary file for number of fencers per school
with open("./static/text/totalFencers.txt") as f:
    for line in f:
        (key, val) = line.strip('\n').split(";")
        fencersPerSchool[key] = val
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

@app.route('/')
def home():
    # Get the information and make the dictionary
    # 2017 final version
    url = 'https://escrimeresults.com/NCAA/ncaa2017.html'
    # ARCHIVED VERSION WORKS
    # url = http://web.archive.org/web/20160325002832/http://www.escrimeresults.com/NCAA/NCAA2016.html
    # EMPTY DOESNT WORK
    # url = http://web.archive.org/web/20160324121938/http://www.escrimeresults.com/NCAA/NCAA2016.html
    s = requests.Session()
    s.mount('https://', MyAdapter())
    page = s.get(url)
    content = pandas.read_html(page.content)
    # Create bouts remain dictionary
    boutsRemain = {}
    # go through list of schools at bottom of page
    if (len(content[-2]) > 2):
        for i in range(1, len(content[-2])):
            schoolColumn = 2
            totalColumn = 3
            remainColumn = 4
            temp = content[-2].iloc[i, schoolColumn].strip('\n')
            # 0: total wins
            # 1: bouts remaining
            # 2: bouts to clinch/bouts behind
            # 3: % of bouts needed to clinch/catch leader
            # 4: name of png for school logo
            # 5: current ranking
            boutsRemain[temp] = [int(content[-2].iloc[i, totalColumn]), int(content[-2].iloc[i, remainColumn]), 0, 0.0, "", 0]
        # {{{
        # ADD A LITTLE FAKE DATA FOR TESTING
        # boutsRemain["Columbia/Barnard"][0] = 163
        # boutsRemain["Ohio State University"][1] = 10
        # boutsRemain["Princeton University"][1] = 20
        # boutsRemain["St. John's University"][1] = 14
        # boutsRemain["Notre Dame"][1] = 20
        # boutsRemain["Lawrence University"][1] = 200
        # }}}
        '''
        how to protect from key error
        if key in dict:
            rank = dict[key]
        else:
        '''
        # sort the bouts and store information in an array
        schools = len(boutsRemain)
        boutsRemain = sorted(boutsRemain.items(), key=lambda i: i[1][0], reverse=True)
        # make sure references to image files are part of array
        # boutsRemain[0][1][4] = schoolConversion[boutsRemain[0][0]] + ".png"
        for i in range (0, schools):
            # make sure references to image files are part of array
            boutsRemain[i][1][4] = schoolConversion[boutsRemain[i][0]] + ".png"
            # what is the current school's place
            boutsRemain[i][1][5] = i + 1
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
                    clinchPercent = round(need / remain * 100.0, 1)
                    if (clinchPercent > 100):
                        boutsRemain[0][1][3] = "Clinch impossible at this point"
                    else:
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
        # get percentage of wins so far
        for i in range (0, schools):
            # current wins / (total - remaining) * 100.0
            totalBouts = (int(fencersPerSchool[boutsRemain[i][0]]) * 23)
            percent = round(boutsRemain[i][1][0] / (totalBouts - boutsRemain[i][1][1]) * 100.0, 1)
            boutsRemain[i][1][0] = str(boutsRemain[i][1][0]) + " (" + str(percent) + "%)"
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
    andrew = random.choice(andrewList)
    elijah = random.choice(elijahList)
    return render_template("about.html", andrew=andrew, elijah=elijah)


if __name__ == "__main__":
    app.run(debug = True)
