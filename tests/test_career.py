import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from tennis_career import get_matches, plot_matches
from tennis_career.career import _clean_matches, _player_id

FIXTURES = Path(__file__).parent
FEMALE = (FIXTURES / "female.js").read_text()
MALE = (FIXTURES / "male.js").read_text()


class CareerTests(unittest.TestCase):
    def test_names(self):
        for name in ["serena williams", "Serena Williams", "SerenaWilliams"]:
            self.assertEqual(_player_id(name), "SerenaWilliams")
        with self.assertRaises(ValueError):
            _player_id("")

    def test_female_ages(self):
        data = _clean_matches(FEMALE, pd.Timestamp("1981-09-26"))
        self.assertEqual(len(data), 3)
        self.assertEqual(data.loc[0, "opponent"], "Anne Miller")
        self.assertAlmostEqual(data.loc[0, "player_age"], 5147 / 365.25)
        self.assertAlmostEqual(data.loc[0, "opponent_age"], 6858 / 365.25)
        self.assertAlmostEqual(data.loc[0, "age_difference"], -1711 / 365.25)

    def test_male_ages(self):
        data = _clean_matches(MALE, pd.Timestamp("1986-06-03"))
        self.assertEqual(len(data), 3)
        self.assertEqual(data.loc[0, "opponent_age"], 22.264202601)
        self.assertAlmostEqual(data.loc[0, "player_age"], 5578 / 365.25)
        self.assertAlmostEqual(data.loc[0, "age_difference"], 5578 / 365.25 - 22.264202601)
        self.assertEqual(data["result"].tolist(), ["L", "L", "W"])

    def test_walkovers_and_missing_ages(self):
        text = FEMALE.replace('"6-1 6-1"', '"W/O"').replace('"19700503"', '""')
        data = _clean_matches(text, pd.Timestamp("1981-09-26"))
        self.assertEqual(len(data), 1)
        self.assertEqual(data.loc[0, "opponent"], "Magui Serna")

    def test_get_matches(self):
        current = "var dob = 19810926;" + FEMALE
        with patch("tennis_career.career._download", side_effect=[current, FEMALE]):
            data = get_matches("serena williams")
        self.assertEqual(len(data), 3)
        self.assertEqual(data.attrs["player"], "serena williams")

    def test_invalid_player(self):
        with patch("tennis_career.career._download", return_value="Player not found"):
            with self.assertRaises(ValueError):
                get_matches("GastonSanchez")

    def test_plot(self):
        data = _clean_matches(MALE, pd.Timestamp("1986-06-03"))
        ax = plot_matches(data)
        self.assertEqual(len(ax.collections[0].get_offsets()), 1)
        self.assertEqual(len(ax.collections[1].get_offsets()), 2)
        plt.close(ax.figure)
