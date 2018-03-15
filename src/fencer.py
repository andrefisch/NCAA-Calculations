class Fencer(object):
    def __init__(self,
            name,
            wins,
            bouts_fenced,
            indicator,
            school_logo):
        self.name = name
        self.wins = wins
        self.bouts_fenced = bouts_fenced
        self.indicator = indicator
        self.school_logo = school_logo

    @property
    def has_bouts_remaining(self):
        return int(self.bouts_fenced) < 23

    @property
    def remaining_bouts(self):
        return 23 - int(self.bouts_fenced)

    @property
    def win_percent(self):
        return "{:.1%}".format(float(self.wins) / float(self.bouts_fenced))
