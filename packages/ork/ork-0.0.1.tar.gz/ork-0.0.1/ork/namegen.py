from .utils import D66
import json
import os


class NameGenerator:
    """
    Psychic Awakenings -based name generator
    """
    # contains the data from name generators published in psychic awakenings during warhammer 40k v8
    data = json.load(open(os.path.join(os.path.dirname(__file__), "namegen.json"), "r"))

    available_factions = {
        faction_name: list(langs)
        for faction_name, langs in data.items()
    }

    @classmethod
    def generate(cls, faction_name, lang):

        assert faction_name in cls.available_factions.keys(), \
            f"faction '{faction_name}' is not available"

        assert lang in cls.available_factions[faction_name], \
            f"lang '{lang}' is not available for faction '{faction_name}'"

        table = cls.data[faction_name][lang]
        front_bit = table[D66()]["front_bit"]
        uvver_bit = table[D66()]["uvver_bit"]

        if uvver_bit is None:
            return front_bit
        else:
            return f"{front_bit} {uvver_bit}"
