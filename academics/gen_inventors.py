from habanero import Crossref

import json
from pprint import pprint,pformat
import csv
import distance
import sys
from collections import defaultdict
import name_norm
import itertools

def select_most_similar_to_name(surname_name_list, f):
    print("!!")
    print(surname_name_list)
    for n in surname_name_list:
        ns = f(n).split()
        print(ns)
        if len(ns)==2:
            if ns[0] in polish_names or ns[1] in polish_names:
                print("#%s->%s"%(pformat(surname_name_list),f(n)))
                return n

    base = max(surname_name_list, key=lambda x: len(f(x)))
    return base

    
def magiclevenshtein(seq1, seqs, max_dist=2, access_fun = lambda x:x):
    for seq2 in seqs:
        dist1 = distance.levenshtein(seq1, access_fun(seq2), max_dist=max_dist)
        if dist1 >= 0:
            yield dist1, seq2


with open("imiona_pl.csv", "r") as f:
    csv1 = csv.reader(f, delimiter=',', quotechar='\'')
    next(csv1, None)
    polish_names  = list(zip(*list(csv1)))[0]

polish_names = name_norm.get_imiona_normalised()



with open('polskie_patenty_z_krotkiej_listy_instytucji_i_ich_wynalazcy.json') as f:
    data = json.load(f)
    



companies =  defaultdict(set) #set()

for pat in data:
    for inventr in pat['inventor_harmonized']:
        companies[pat['assignee_alias']].add(inventr['name'])


invent_names = sorted(list(itertools.chain.from_iterable(companies.values())))
#invent_names = invent_names[:1000]

invent_names_clean = dict()

for name in invent_names:
    name_c = name
    name = name_norm.inventor_name_normalise(name)
    invent_names_clean[name_c] = name
    print(name_c+"->"+name)   



name_aliases = list()

invent_names_clean_tmp = set(list(invent_names_clean.items()))
print("@@@2")
pprint(invent_names_clean_tmp)

#invent_names_clean_tmp.discard("")
c=0
print("@@@1")
while len(invent_names_clean_tmp)>0:
    c=c+1
    name = invent_names_clean_tmp.pop()

    p1 = list(zip(*sorted(magiclevenshtein(name[1], invent_names_clean_tmp, max_dist=1, access_fun=lambda x:x[1]))))
    p2 = []#list(zip(*sorted(magiclevenshtein(name[0], invent_names_clean_tmp, max_dist=1, access_fun=lambda x:x[1]))))

    print("%d/%d %s->%s"%(c, len(invent_names_clean_tmp), name, pformat(p1)))
    print("%d/%d %s->%s"%(c, len(invent_names_clean_tmp), name, pformat(p2)))

    if len(p1)==0 and len(p2)==0 :
        name_aliases.append(name)
        continue

    p = set()    
    if len(p1)==2:
        p = set(p1[1])
    if len(p2)==2:
        p = p | set(p2[1])

    similar = list(p) + [name]

    base = select_most_similar_to_name(similar, lambda x:x[1])

    for s in similar:
        name_aliases.append((s[0],base[1]))
        invent_names_clean_tmp.discard(s)
    sys.stdout.flush()
       
name_aliases.sort( key = lambda x:x[0])
pprint(name_aliases)
print("@@@#")

with open('inventors_w_aliases.csv',"w") as csvfile:
    writer = csv.writer(csvfile,)
    writer.writerow(("inventor_raw","inventor_alias"))
    subs = name_aliases
    writer.writerows(subs)




    

