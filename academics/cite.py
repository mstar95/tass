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
from pprint import pprint

import distance

def inlevenshtein(seq1, seqs, max_dist=0.1):
    for seq2 in seqs:
        dist1 = distance.levenshtein(seq1, seq2, max_dist=2)
        if dist1 !=-1:
            dist2 = distance.nlevenshtein(seq1, seq2, )
            if dist2 <= max_dist:
                yield dist2, seq2


with open('polskie_patenty_z_krotkiej_listy_instytucji_i_ich_wynalazcy.json') as f:
    data = json.load(f)
    
#pprint(data)

from collections import defaultdict
#d = defaultdict(set)
companies =  defaultdict(set) #set()

for pat in data:
    for inventr in pat['inventor_harmonized']:
        companies[pat['assignee_alias']].add(inventr['name'])

pprint(companies)
co_names = sorted(companies.keys())

co_names = sorted(companies.keys())

for name in co_names:
    pprint(sorted(distance.ilevenshtein(name, co_names, max_dist=2)))



    

