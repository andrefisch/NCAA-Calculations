from school import School
from ranking import Ranking


SCHOOL_COLUMN = 2
TOTAL_COLUMN = 3
REMAINING_BOUTS_COLUMN = 4
BOUTS_PER_FENCER = 23


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
    return len(content[-2]) > 2


def _get_schools_from_content(content,
                              school_map,
                              school_fencers_map):
    schools = []

    for i in range(1, len(content[-2])):
        school_name = content[-2].iloc[i, SCHOOL_COLUMN].strip('\n')
        wins = int(content[-2].iloc[i, TOTAL_COLUMN])
        remaining_bouts = int(content[-2].iloc[i, REMAINING_BOUTS_COLUMN])
        total_bouts = int(school_fencers_map[school_name]) * BOUTS_PER_FENCER
        school_logo = "%s.png" % school_map[school_name]

        school = School(school_name,
                        wins,
                        remaining_bouts,
                        total_bouts,
                        school_logo)
        schools.append(school)

    return schools
