class Fencer(object):
    def __init__(self,
                 name,
                 school,
                 wins,
                 bouts_fenced):
        self.name = name
        self.school = school
        self.wins = wins
        self.bouts_fenced = bouts_fenced

    def will_finish_higher(self, other_school):
        return (self.wins - other_school.wins) > other_school.remaining_bouts

    def wins_to_clinch_over(self, other_school):
        return other_school.remaining_bouts - (self.wins - other_school.wins) + 1

    @property
    def has_bouts_remaining(self):
        return self.remaining_bouts > 0

    @property
    def win_percent(self):
        return "{:.1%}".format(float(self.wins) / self.total_bouts)
