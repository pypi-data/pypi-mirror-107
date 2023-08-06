# Ork

[![Actions Status](https://github.com/bonnal-enzo/ork/workflows/test/badge.svg)](https://github.com/bonnal-enzo/ork/actions) [![Actions Status](https://github.com/bonnal-enzo/ork/workflows/PyPI/badge.svg)](https://github.com/bonnal-enzo/ork/actions)

## Install

`pip3 install ork`

## Usage

```python
>>> from ork.namegen import NameGenerator
>>> NameGenerator.generate(faction_name="orks", lang="en")
Snarkrat Wurldkilla
>>> NameGenerator.generate(faction_name="orks", lang="fr")
Droknog Botte lé Fess'
>>> NameGenerator.generate(faction_name="space wolves", lang="en")
Berek Wyrdfang
>>> NameGenerator.generate(faction_name="space wolves", lang="fr")
Leif Le Berserk
```
