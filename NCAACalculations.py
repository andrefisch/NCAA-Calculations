
# coding: utf-8

# In[99]:

import pandas
import operator


# In[100]:

# Get the information and make the dictionary
html = pandas.read_html("http://escrimeresults.com/NCAA/ncaa2016.html")


# In[101]:

# Read schools into dictionary
# works correctly #############################################################
schools = {}
schoolColumn = 0
victoryColumn = 27
otherFencers = 23
# go through each row of the table with a fencer in it
for i in range(1, 25):
    # go through each of the six tables
    for j in range (1, 7):
        # go through the pool tables and get the school names
        temp = html[j * 3 - 1].iloc[i, schoolColumn].strip('\n')
        # if school name is in dictionary, increase their total number of bouts
        if (temp in schools.keys()):
            schools[temp] = [schools[temp][0], schools[temp][1] + otherFencers]
        # if the school name isnt in dictionary add it to the dictionary
        else:
            schools[temp] = [0, otherFencers]
        # find victories for the fencer
        num = html[j * 3 - 1].iloc[i, victoryColumn]
        # and add it to their school
        schools[temp] = [schools[temp][0] + int(num), schools[temp][1]]
###############################################################################
# sort by total wins
schoolTotal = len(schools.keys())
schools = sorted(schools.items(), key=lambda i: i[1][0], reverse=True)
# print the school data
for p in schools: 
    print (p)
#for key, value in schools.items() :
#    print (key, value)


# In[102]:

# Import the dictionary file
schoolConversion = {}
with open("schoolDict.txt") as f:
    for line in f:
       (key, val) = line.strip('\n').split(";")
       schoolConversion[key] = val
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
boutsRemain["Columbia/Barnard"][1] = 10
boutsRemain["Ohio State University"][1] = 6
boutsRemain["Princeton University"][1] = 10
for key, value in boutsRemain.items():
    print (key, value)


# In[103]:

schoolToCheck = "PRIN"
firstPlace = ""
secondPlace = ""
xthPlace = ""
# schools
#     SCHOOLCODE => [Total wins, total bouts]
# schoolConversion
#     SCHOOLCODE => Schoolname
# boutsRemain
#     Schoolname => [Total wins, bouts remain]

# 1. Find winner and schoolToCheck place
# 2. Is schoolToCheck winner? 
# 3.     Yes -> find second place school
#               "schoolToCheck is in first place, ahead of secondPlace by (firstWins - secondWins)"
# 3.     No  -> "schoolToCheck is in xthPlace and is (firstWins - xthWins) behind firstSchool

# 1. Find winner and schoolToCheck place
for i in range(1, 25):
    schoolColumn = 2
    school = html[18].iloc[i, schoolColumn]
    # who is in first place
    if (i == 1):
        firstPlace = school.strip('\n')
    # who is in second place
    elif (i == 2):
        secondPlace = school.strip('\n')
    # what place is our school in
    if (schoolConversion[schoolToCheck] == school):
        xthPlace = i
# If we are in first place
if (xthPlace == 1):
    diff = int(boutsRemain[firstPlace][0]) - int(boutsRemain[secondPlace][0])
    if (diff > int(boutsRemain[secondPlace][1])):
        print (firstPlace + " is in first place, ahead of " + secondPlace + " by " + str(diff) + " bouts and has clinched the championship!")
    else:
        # (second place's win total + second place's remaining bouts) - first place total bouts
        need = (int(boutsRemain[secondPlace][1]) + int(boutsRemain[secondPlace][0])) - int(boutsRemain[firstPlace][0])
        remain = int(boutsRemain[firstPlace][1])
        percent = need / remain * 100.0
        print (firstPlace + " is in first place, ahead of " + secondPlace + " by " + str(diff) + " bouts and needs to win " + str(need) + " of their " + str(remain) + " remaining bouts to clinch. That's " + str(percent) + "% of their remaining bouts.")
# If we are not in first place
else:
    diff = int(boutsRemain[firstPlace][0]) - int(boutsRemain[schoolConversion[schoolToCheck]][0])
    #weNeed = (int(boutsRemain[schoolConversion[schoolToCheck]][1]) + int(boutsRemain[schoolConversion[schoolToCheck]][0])) - int(boutsRemain[firstPlace][0])
    weRemain = int(boutsRemain[schoolConversion[schoolToCheck]][1])
    wePercent = diff / weRemain * 100.0
    theyNeed = 1 + (int(boutsRemain[secondPlace][1]) + int(boutsRemain[secondPlace][0])) - int(boutsRemain[firstPlace][0])
    theyRemain = int(boutsRemain[firstPlace][1])
    theyPercent = theyNeed / theyRemain * 100.0
    # OSU is in second place and needs to win 7 of their 10 remaining bouts to catch Columbia/Barnard.  
    # That's 70% of their remaining bouts.  If Columbia/Barnard wins 3 of their ten remaining bouts, 
    # OSU will be eliminated.
    if (diff > int(boutsRemain[schoolConversion[schoolToCheck]][1])):
        print (str(schoolConversion[schoolToCheck]) + " is in " + str(xthPlace) + " place and is " + str(diff) + " bouts behind " + firstPlace)
        print ("Because " + schoolToCheck + " needs to win " + str(diff) + " bouts to catch " + firstPlace + " and only has " + str(weRemain) + " bouts left to fence,")
        print (schoolToCheck + " cannot catch " + firstPlace)
    else:
        print (str(schoolConversion[schoolToCheck]) + " is in " + str(xthPlace) + " place and is " + str(diff) + " bouts behind " + firstPlace)
        print (schoolToCheck + " needs to win " + str(diff) + " of their " + str(weRemain) + " remaining bouts to catch " + firstPlace + ". That's " + str(wePercent) + "% of their remaining bouts")  
        print ("If " + firstPlace + " wins " + str(theyNeed) + " of their remaining " + str(theyRemain) + " bouts (" + str(theyPercent) + "%) " + schoolToCheck + " will be eliminated")

