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
    data = ResultService.get_current_results()
    return render_template("home.html", boutsRemain=data)

@app.route('/about/')
def about():
    andrew = random.choice(andrewList)
    elijah = random.choice(elijahList)
    return render_template("about.html", andrew=andrew, elijah=elijah)


if __name__ == "__main__":
    app.run(debug = True)
