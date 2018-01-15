def scrape_site_content_for_bout_data(content,
                                      school_map,
                                      school_fencers_map):
    remaining_bout_data = {}
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
            remaining_bout_data[temp] = [int(content[-2].iloc[i, totalColumn]), int(content[-2].iloc[i, remainColumn]), 0, 0.0, "", 0]
        # {{{
        # ADD A LITTLE FAKE DATA FOR TESTING
        # remaining_bout_data["Columbia/Barnard"][0] = 163
        # remaining_bout_data["Ohio State University"][1] = 10
        # remaining_bout_data["Princeton University"][1] = 20
        # remaining_bout_data["St. John's University"][1] = 14
        # remaining_bout_data["Notre Dame"][1] = 20
        # remaining_bout_data["Lawrence University"][1] = 200
        # }}}
        '''
        how to protect from key error
        if key in dict:
            rank = dict[key]
        else:
        '''
        # sort the bouts and store information in an array
        schools = len(remaining_bout_data)
        remaining_bout_data = sorted(remaining_bout_data.items(), key=lambda i: i[1][0], reverse=True)
        # make sure references to image files are part of array
        # remaining_bout_data[0][1][4] = school_map[remaining_bout_data[0][0]] + ".png"
        for i in range (0, schools):
            # make sure references to image files are part of array
            remaining_bout_data[i][1][4] = school_map[remaining_bout_data[i][0]] + ".png"
            # what is the current school's place
            remaining_bout_data[i][1][5] = i + 1
        # find win differences in wins for teams and fill out array information 
        isOver = True
        for i in range (1, schools):
            # if the difference is greater than all other schools' remaining bouts to fence then it is over
            diff = int(remaining_bout_data[0][1][0]) - int(remaining_bout_data[i][1][0])
            if (diff < int(remaining_bout_data[i][1][1])):
                isOver = False
                # bouts needed to clinch for top school becomes ith place's win total + ith place's remaining bouts - 1st place total bouts
                need = 1 + int(remaining_bout_data[i][1][0]) + int(remaining_bout_data[i][1][1]) - int(remaining_bout_data[0][1][0])
                remain = int(remaining_bout_data[0][1][1])
                if (remain > 0):
                    remaining_bout_data[0][1][2] = need
                    clinchPercent = round(need / remain * 100.0, 1)
                    if (clinchPercent > 100):
                        remaining_bout_data[0][1][3] = "Clinch impossible at this point"
                    else:
                        remaining_bout_data[0][1][3] = str(round(need / remain * 100.0, 1)) + "%"
                else:
                    remaining_bout_data[0][1][2] = "DONE"
                    remaining_bout_data[0][1][3] = "DONE"
                break
        if (isOver):
            remaining_bout_data[0][1][2] = "WINNER OF THE 2017"
            remaining_bout_data[0][1][3] = "NCAA FENCING CHAMPIONSHIP!!"
        for i in range (1, schools):
            # win difference
            diff = int(remaining_bout_data[0][1][0]) - int(remaining_bout_data[i][1][0])
            # 
            iRemain = int(remaining_bout_data[i][1][1])
            firstNeed = 1 + (int(remaining_bout_data[i][1][1]) + int(remaining_bout_data[i][1][0])) - int(remaining_bout_data[0][1][0])
            firstRemain = int(remaining_bout_data[0][1][1])
            # firstPercent = firstNeed / firstRemain * 100.0
            if (diff > int(remaining_bout_data[i][1][1])):
                remaining_bout_data[i][1][2] = diff
                remaining_bout_data[i][1][3] = "OUT"
            else:
                if (iRemain > 0):
                    iPercent = round(diff / iRemain * 100.0, 1)
                    remaining_bout_data[i][1][2] = diff
                    remaining_bout_data[i][1][3] = str(iPercent) + "%"
                else:
                    remaining_bout_data[i][1][2] = diff
                    remaining_bout_data[i][1][3] = "OUT"
        # get percentage of wins so far
        for i in range (0, schools):
            # current wins / (total - remaining) * 100.0
            totalBouts = (int(school_fencers_map[remaining_bout_data[i][0]]) * 23)
            percent = round(remaining_bout_data[i][1][0] / (totalBouts - remaining_bout_data[i][1][1]) * 100.0, 1)
            remaining_bout_data[i][1][0] = str(remaining_bout_data[i][1][0]) + " (" + str(percent) + "%)"
        # for i in range(0, schools):
            # if (int(remaining_bout_data[i][1][1]) == 0):
                # remaining_bout_data[i][1][1] == "DONE"
                # print ("Changed bouts remain for " + remaining_bout_data[i][0] + " to " + str(remaining_bout_data[i][1][1]))
    else:
        print ("derp...")

    return remaining_bout_data
