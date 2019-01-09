from habanero import Crossref

"""
cr = Crossref(mailto = "jedr.ka@gmail.com")
x = cr.works(query_author = "Andrzej Karbowski")
x['message']
x['message']['total-results']
x['message']['items']

import distance
distance.nlevenshtein(s,s)
"""

import json
from pprint import pprint,pformat
import csv
import distance
import sys
import itertools
import unicodedata

from collections import defaultdict
with open('polskie_patenty_z_krotkiej_listy_instytucji_i_ich_wynalazcy.json') as f:
    data = json.load(f)
    



