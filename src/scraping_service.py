from school import School
from ranking import Ranking


SCHOOL_COLUMN = 2
TOTAL_COLUMN = 3
REMAINING_BOUTS_COLUMN = 4


def scrape_site_content_for_bout_data(content,
                                      school_map,
                                      school_fencers_map):
    if not _has_content(content):
        raise Exception(message="No content found") # TODO, raise more specific error

    remaining_bout_data = _get_school_data(content=content)

    schools = len(remaining_bout_data)

    remaining_bout_data = _update_current_school_rankings(remaining_bout_data)
    remaining_bout_data = _clean_references_to_image_files(remaining_bout_data,
                                                           school_map)
    remaining_bout_data = _calculate_win_differences(remaining_bout_data)
    remaining_bout_data = _calculate_win_percentages(remaining_bout_data,
                                                     school_fencers_map)

    return remaining_bout_data


def _has_content(content):
    return len(content[-2]) > 2


def _get_school_data(content):
    remaining_bout_data = {}

    for i in range(1, len(content[-2])):
        school = content[-2].iloc[i, SCHOOL_COLUMN].strip('\n')
        remaining_bout_data[school] = [
            int(content[-2].iloc[i, TOTAL_COLUMN]),
            int(content[-2].iloc[i, REMAINING_BOUTS_COLUMN]),
            0,
            0.0,
            "",
            0]

    return remaining_bout_data


def _update_current_school_rankings(remaining_bout_data):
    remaining_bout_data = sorted(remaining_bout_data.items(), key=lambda i: i[1][0], reverse=True)
    for school_index in xrange(len(remaining_bout_data)):
        remaining_bout_data[school_index][1][5] =  school_index + 1

    return remaining_bout_data


def _clean_references_to_image_files(remaining_bout_data,
                                     school_map):
    for school_index in xrange(len(remaining_bout_data)):
        remaining_bout_data[school_index][1][4] = school_map[remaining_bout_data[school_index][0]] + ".png"

    return remaining_bout_data


def _calculate_win_differences(remaining_bout_data):
    isOver = True
    for school_index in xrange(1, len(remaining_bout_data)):
        # if the difference is greater than all other schools' remaining bouts to fence then it is over
        diff = int(remaining_bout_data[0][1][0]) - int(remaining_bout_data[school_index][1][0])
        if (diff < int(remaining_bout_data[school_index][1][1])):
            isOver = False
            # bouts needed to clinch for top school becomes ith place's win total + ith place's remaining bouts - 1st place total bouts
            need = 1 + int(remaining_bout_data[school_index][1][0]) + int(remaining_bout_data[school_index][1][1]) - int(remaining_bout_data[0][1][0])
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
    for school_index in xrange(1, len(remaining_bout_data)):
        # win difference
        diff = int(remaining_bout_data[0][1][0]) - int(remaining_bout_data[school_index][1][0])
        # 
        iRemain = int(remaining_bout_data[school_index][1][1])
        firstNeed = 1 + (int(remaining_bout_data[school_index][1][1]) + int(remaining_bout_data[school_index][1][0])) - int(remaining_bout_data[0][1][0])
        firstRemain = int(remaining_bout_data[0][1][1])
        # firstPercent = firstNeed / firstRemain * 100.0
        if (diff > int(remaining_bout_data[school_index][1][1])):
            remaining_bout_data[school_index][1][2] = diff
            remaining_bout_data[school_index][1][3] = "OUT"
        else:
            if (iRemain > 0):
                iPercent = round(diff / iRemain * 100.0, 1)
                remaining_bout_data[school_index][1][2] = diff
                remaining_bout_data[school_index][1][3] = str(iPercent) + "%"
            else:
                remaining_bout_data[school_index][1][2] = diff
                remaining_bout_data[school_index][1][3] = "OUT"


    return remaining_bout_data


def _calculate_win_percentages(remaining_bout_data,
                               school_fencers_map):
    for school_index in xrange(len(remaining_bout_data)):
        totalBouts = (int(school_fencers_map[remaining_bout_data[school_index][0]]) * 23)
        percent = round(remaining_bout_data[school_index][1][0] / (totalBouts -
                                                                   remaining_bout_data[school_index][1][1]) * 100.0,
                        1)
        remaining_bout_data[school_index][1][0] = str(remaining_bout_data[school_index][1][0]) + " (" + str(percent) + "%)"

    return remaining_bout_data
