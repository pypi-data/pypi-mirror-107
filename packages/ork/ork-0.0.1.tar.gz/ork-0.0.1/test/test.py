import unittest

import sys

sys.path.append("..")

from ork.namegen import NameGenerator


class Test(unittest.TestCase):
    def test_right_cases(self):
        for faction_name in NameGenerator.available_factions.keys():
            for lang in NameGenerator.available_factions[faction_name]:
                print(NameGenerator.generate(faction_name=faction_name, lang=lang))

    def test_unavailable_lang(self):
        self.assertRaises(AssertionError, lambda: NameGenerator.generate(faction_name="orks", lang="it"))
