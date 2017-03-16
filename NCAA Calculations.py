
# coding: utf-8

# In[1]:

import pandas
import operator


# In[14]:

# Get the information and make the dictionary
html = pandas.read_html("http://escrimeresults.com/NCAA/ncaa2016.html")


# In[39]:

# Read schools into dictionary
# works correctly #############################################################
schools = {}
schoolColumn = 0
victoryColumn = 27
otherFencers = 23
for i in range(1, 25):
    for j in range (1, 7):
        temp = html[j * 3 - 1].iloc[i, schoolColumn].strip('\n')
        if (temp in schools.keys()):
            schools[temp] = [schools[temp][0], schools[temp][1] + otherFencers]
        else:
            schools[temp] = [0, otherFencers]
        num = html[j * 3 - 1].iloc[i, victoryColumn]
        schools[temp] = [schools[temp][0] + int(num), schools[temp][1]]
###############################################################################
schools = sorted(schools.items(), key=lambda i: i[1][0], reverse=True)

for p in schools: 
    print (p)
#for key, value in schools.items() :
#    print (key, value)


# In[42]:

# Import the dictionary file
schoolConversion = {}
with open("schoolDict.txt") as f:
    for line in f:
       (key, val) = line.strip('\n').split(";")
       schoolConversion[key] = val
#for key, value in schoolConversion.items():
#    print (key, value)
#print (html[18].iloc[1, 2])
# Create bouts remain dictionary
boutsRemain = {}
for i in range(1, 25):
    schoolColumn = 2
    totalColumn = 3
    remainColumn = 4
    temp = html[18].iloc[i, schoolColumn].strip('\n')
    if (temp in boutsRemain.keys()):
        boutsRemain[temp] = [boutsRemain[temp][0], boutsRemain[temp][1] + otherFencers]
    else:
        boutsRemain[temp] = [html[18].iloc[i, totalColumn], html[18].iloc[i, remainColumn]]
# html[18]
for key, value in boutsRemain.items():
    print (key, value)


# In[51]:

schoolToCheck = "OSU"
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
print (schoolToCheck + " is in " + str(xthPlace))
if (xthPlace == 1):
    diff = int(boutsRemain[firstPlace][0]) - int(boutsRemain[secondPlace][0])
    print (firstPlace + " is in first place, ahead of " + secondPlace + " by " + str(diff))
else:
    diff = int(boutsRemain[firstPlace][0]) - int(boutsRemain[secondPlace][0])
    print (str(schoolConversion[schoolToCheck]) + " is in " + str(xthPlace) + " place and is " + str(diff) + " bouts behind " + firstPlace) 


# In[ ]:



