from habanero import Crossref

import json
from pprint import pprint,pformat
import csv
import distance
import sys

import unicodedata

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
    
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

import itertools
invent_names = sorted(list(itertools.chain.from_iterable(companies.values())))


trash_subst = "DR INZ INŻ ING DIPL-ING DIPL DR-ING PROF CHEM MD M SC SURGE ENG DR-CHEM".split()
invent_names_clean = []

for name in invent_names:
    name_c=name
    name=strip_accents(name)
    name=" %s "%name.upper()
    name=name.replace(",","")
    name=name.replace("\"","")
    for sbst in trash_subst:
        name=name.replace(" "+sbst+" ", " ")
        name = " ".join(name.strip().split()[:2])
    invent_names_clean.append(name)
    print(name_c+"->"+name)   



name_aliases = dict()
#invent_names_clean = invent_names_clean[:10]

invent_names_clean_tmp = set(invent_names_clean)

#for c,name in enumerate(set(invent_names_clean)):
invent_names_clean_tmp.discard("")
c=0
while len(invent_names_clean_tmp)>0:
    c=c+1
    name = invent_names_clean_tmp.pop()
    if True:
        p = list(zip(*sorted(distance.ilevenshtein(name, invent_names_clean_tmp, max_dist=1))))
        print("%d/%d %s->%s"%(c,len(invent_names_clean_tmp),name,pformat(p)))
        if(len(p)==0):
            name_aliases[name] = name 
            continue
        similar = p[1]
        base = max(similar, key=len)
        name_aliases[base] = base
        for s in similar:
            name_aliases[s] = base
            invent_names_clean_tmp.discard(s)
   
        
    sys.stdout.flush()
            

pprint(name_aliases)

with open('inventors_w_aliases.csv',"w") as csvfile:
    writer = csv.writer(csvfile,)
    writer.writerow(("inventor_raw","inventor_alias"))
    subs = list(name_aliases.items())
    subs.sort()
    writer.writerows(subs)




    

