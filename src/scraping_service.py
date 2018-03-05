from school import School
from ranking import Ranking


SCHOOL_COLUMN = 2
TOTAL_COLUMN = 3
REMAINING_BOUTS_COLUMN = 4
BOUTS_PER_FENCER = 23
COMBINED_TABLE = -2


def scrape_site_content_ranking_data(content,
                                     school_map,
                                     school_fencers_map):
    if not _has_content(content):
        raise Exception(message="No content found") # TODO, raise more specific error

    schools = _get_schools_from_content(content,
                                        school_map,
                                        school_fencers_map)
    ranking = Ranking(schools)

    return ranking

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
            total_bouts = int(school_fencers_map[school_name]) * BOUTS_PER_FENCER
        else:
            total_bouts = 1
        if school_name in school_map:
            school_logo = "%s.png" % school_map[school_name]
        else:
            school_logo = "NCAA.png"

        school = School(school_name,
                        wins,
                        remaining_bouts,
                        total_bouts,
                        school_logo)
        schools.append(school)

    return schools
