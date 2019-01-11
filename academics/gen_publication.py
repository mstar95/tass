from habanero import Crossref

import csv
import json

def safeGetTitle(x):
    return x[0] if x else None

with open('inventors_w_aliases.csv',"r") as csvfile:
    csv_inventors = csv.reader(csvfile, delimiter=',')
    data  = list(csv_inventors)

aliases = list(set([x[1] for x in data[2:]]))
aliases.sort()

cr = Crossref(mailto = "jedr.ka@gmail.com")
publications = dict()
counter = 0
for alias in aliases:
    counter = counter + 1
    print(alias, counter)
    res = cr.works(query_author = alias)
    publications[alias] = list(filter(None, [ safeGetTitle(x.get('title')) for x in res['message']['items'] ]))
    if counter % 5:
        with open('publikacjeDir/pub' + str(counter / 5) + '.json',"w") as jsonfile:
            json.dump(publications, jsonfile)
    
    publications = dict()


