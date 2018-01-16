from unittest import TestCase

from school import School


class TestSchool(TestCase):
    def test_init_school(self):
        school = School(name="school",
                        wins=32,
                        remaining_bouts=40,
                        total_bouts=72,
                        school_logo="logo.png")

        self.assertEqual(school.name, "school")
        self.assertEqual(school.wins, 32)
        self.assertEqual(school.remaining_bouts, 40)
        self.assertEqual(school.total_bouts, 72)
        self.assertEqual(school.school_logo, "logo.png")

    def test_will_finish_higher(self):
        school1= School(name="school",
                        wins=5,
                        remaining_bouts=5,
                        total_bouts=10,
                        school_logo="logo.png")
        school2= School(name="school",
                        wins=3,
                        remaining_bouts=1,
                        total_bouts=10,
                        school_logo="logo.png")

        self.assertTrue(school1.will_finish_higher(school2))
        self.assertFalse(school2.will_finish_higher(school1))

    def test_wins_to_clinch_over(self):
        school1= School(name="school",
                        wins=5,
                        remaining_bouts=5,
                        total_bouts=10,
                        school_logo="logo.png")
        school2= School(name="school",
                        wins=5,
                        remaining_bouts=3,
                        total_bouts=10,
                        school_logo="logo.png")

        self.assertEqual(school1.wins_to_clinch_over(school2),
                         4)

    def test_has_bouts_remaining(self):
        school= School(name="school",
                       wins=5,
                       remaining_bouts=5,
                       total_bouts=10,
                       school_logo="logo.png")

        self.assertTrue(school.has_bouts_remaining)

        school.remaining_bouts = 0
        self.assertFalse(school.has_bouts_remaining)

    def test_win_percent(self):
        school = School(name="school",
                       wins=3,
                       remaining_bouts=0,
                       total_bouts=9,
                       school_logo="logo.png")

        self.assertEqual(school.win_percent,
                         "33.3%")


