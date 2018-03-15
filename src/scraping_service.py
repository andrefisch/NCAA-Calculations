from school import School
from fencer import Fencer
from ranking import Ranking


SCHOOL_COLUMN = 2
TOTAL_COLUMN = 3
REMAINING_BOUTS_COLUMN = 4
BOUTS_PER_FENCER = 23
COMBINED_TABLE = -2


def scrape_site_content_ranking_data(content,
                                     school_map,
                                     school_fencers_map,
                                     year):
    if not _has_content(content):
        raise Exception(message="No content found") # TODO, raise more specific error

    schools = _get_schools_from_content(content,
                                        school_map,
                                        school_fencers_map)
    fencers = _get_fencers_from_content(content, school_map)
    ranking = Ranking(schools, year)

    return (ranking, fencers)

def _has_content(content):
    return len(content[COMBINED_TABLE]) > 2


def _get_schools_from_content(content,
                              school_map,
                              school_fencers_map):
    schools = []

    for i in range(1, len(content[COMBINED_TABLE])):
        school_name = content[COMBINED_TABLE].iloc[i, SCHOOL_COLUMN].strip('\n').encode("ascii", "ignore")
        wins = int(content[COMBINED_TABLE].iloc[i, TOTAL_COLUMN])
        remaining_bouts = int(content[COMBINED_TABLE].iloc[i, REMAINING_BOUTS_COLUMN])
        if school_name in school_fencers_map:
            total_fencers = int(school_fencers_map[school_name])
        else:
            total_fencers = 1
        total_bouts = total_fencers * BOUTS_PER_FENCER
        if school_name in school_map:
            school_logo = "%s.png" % school_map[school_name]
        else:
            school_logo = "NCAA.png"

        school = School(school_name,
                        total_fencers,
                        wins,
                        remaining_bouts,
                        total_bouts,
                        school_logo)
        schools.append(school)

    return schools

def _get_fencers_from_content(content, school_map):
    fencers = []
    for j in range (0, len(content) - 2):
        weapon = []
        for i in range (1, len(content[j][2])):
            name = str(content[j][2][i])
            school_name = str(content[j][3][i])
            if school_name in school_map:
                school_logo = "%s.png" % school_map[school_name]
            else:
                school_logo = "NCAA.png"
            try:
                wins, bouts_fenced = str(content[j][4][i]).split('/')
            except:
                break
            indicator = str(content[j][8][i])

            fencer = Fencer(name,
                            wins,
                            bouts_fenced,
                            indicator,
                            school_logo)

            # fencers.append(fencer)
            weapon.append(fencer)
        fencers.append(weapon)

    return [x for x in fencers if x != []]
