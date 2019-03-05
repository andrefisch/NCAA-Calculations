class Ranking(object):
    def __init__(self, schools, year):
        self.schools = sorted(schools,
                              key=lambda x: x.wins,
                              reverse=True)
        self.year = year

    @property
    def is_over(self):
        return all(map(self.first_place.will_finish_higher,
                       self.trailing_schools))

    @property
    def first_place(self):
        return self.schools[0]

    @property
    def trailing_schools(self):
        return self.schools[1:]

    @property
    def percent_remaining_bouts_leader_needs_to_clinch(self):
        percent_wins =  (float(self.bouts_leader_needs_to_clinch) /
                         self.first_place.remaining_bouts)
        return "{:.1%}".format(percent_wins)

    def bouts_behind_leader(self, school):
        return self.first_place.wins - school.wins

    @property
    def leader_can_clinch(self):
        return self.bouts_leader_needs_to_clinch <= self.first_place.remaining_bouts

    @property
    def bouts_leader_needs_to_clinch(self):
        return max(map(self.first_place.wins_to_clinch_over,
                       self.trailing_schools))

    def is_school_out(self, school):
        return self.first_place.will_finish_higher(school)
