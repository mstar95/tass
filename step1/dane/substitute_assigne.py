from collections import defaultdict
import distance
from pprint import pprint
import csv


def inlevenshtein(seq1, seqs, max_dist=0.1):
    for seq2 in seqs:
        dist1 = distance.levenshtein(seq1, seq2, max_dist=2)
        if dist1 !=-1:
            dist2 = distance.nlevenshtein(seq1, seq2, )
            if dist2 <= max_dist:
                yield dist2, seq2



f = open("lista_polskich_assignee.csv", "r")
csv1 = csv.reader(f, delimiter=',')
next(csv1, None)
dirty_names_all  = list(zip(*list(csv1)))[0]



f2 = open("krotka_lista_polskich_assignee_min6.csv", "r")
csv2 = csv.reader(f2, delimiter=',')
next(csv2, None)
dirty_names_short   = list(zip(*list(csv2)))[0]


names_substitutions = dict()



limit = -1
for c,name in enumerate(dirty_names_short):
    if name not in names_substitutions:
        similar = zip(*sorted(inlevenshtein(name, dirty_names_all, max_dist=0.13)))

        similar = list(similar)
        print(similar)
        similar=similar[1]
        _names_substitutions = dict()
        for name_synonyme in similar:
            if name != similar:
                _names_substitutions[name_synonyme] = name
        print("%d/%d"%(c,len(dirty_names_short)))
        pprint(_names_substitutions)
        names_substitutions = {**names_substitutions,**_names_substitutions}
    if limit == 0:
        break
    limit = limit-1
    
pprint(names_substitutions)

with open('lista_polskich_assignee_w_aliases.csv',"w") as csvfile:
    writer = csv.writer(csvfile,)
    writer.writerow(("assignee_raw","assignee_alias"))
    
    subs = list(names_substitutions.items())
    subs.sort()
    writer.writerows(subs)
    
    
    
    
    
    
       
