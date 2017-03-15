import pandas
import operator

#Get the information and make the dictionary
html = pandas.read_html("http://escrimeresults.com/NCAA/ncaa2016.html")

# Read schools into dictionary
# works correctly #######################################################
schools = {}
schoolColumn = 0
victoryColumn = 27
otherFencers = 23
for i in range(1, 25):
    for j in range (1, 7):
        temp = html[j * 3 - 1].iloc[i, schoolColumn]
        if (temp in schools.keys()):
            schools[temp] = [schools[temp][0], schools[temp][1] + otherFencers]
        else:
            schools[temp] = [0, otherFencers]
        num = html[j * 3 - 1].iloc[i, victoryColumn]
        schools[temp] = [schools[temp][0] + int(num), schools[temp][1]]
#########################################################################
schools = sorted(schools.items(), key=lambda i: i[1][0], reverse=True)
for p in schools: 
    print (p)
