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

class SetEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return json.JSONEncoder.default(self, obj)



from collections import defaultdict
with open('polskie_patenty_z_krotkiej_listy_instytucji_i_ich_wynalazcy.json') as f:
    data = json.load(f)
    
with open('inventors_w_aliases.csv',"r") as csvfile:
    csv_inventors = csv.reader(csvfile, delimiter=',')
    inventors_names_w_aliases  = list(csv_inventors)

pprint(inventors_names_w_aliases)

with open('lista_polskich_assignee_w_aliases.csv',"r") as csvfile:
    csv_assignee = csv.reader(csvfile, delimiter=',')
    assignee_names_w_aliases  = list(csv_assignee)


pprint(assignee_names_w_aliases)

inventors_alias_dict = dict(inventors_names_w_aliases)
assignee_alias_dict = dict(assignee_names_w_aliases)

aliased_patents = []

for patent in data:

    #pprint(patent)
    inventors_aliases = []
    for inventor in patent["inventor_harmonized"]:
        name = inventor["name"]
        alias = inventors_alias_dict[name]
        inventors_aliases.append(alias)
    
    c_patent = dict() 
    c_patent["inventor_aliased"] = inventors_aliases
    
    """
    assignee_aliases = []
    for assignee in patent["assignee_harmonized"]:
        name = assignee["name"]
        alias = assignee_alias_dict[name]
        assignee_aliases.append(alias)
    
    patent["assignee_aliased"] = inventors_aliases
    """
    c_patent["assignee_alias"] = patent["assignee_alias"]
    aliased_patents.append(c_patent)

pprint(aliased_patents)


with open('aliased_patents.json',"w") as jsonfile:
    json.dump(aliased_patents, jsonfile)
    

assignee_inventor_dict = defaultdict(set)

for patent in aliased_patents:
    for inventor in patent["inventor_aliased"]:
        assignee_inventor_dict[patent["assignee_alias"]].add(inventor)
	
with open('cooperation_assignee.json',"w") as jsonfile:
    json.dump(assignee_inventor_dict, jsonfile,cls=SetEncoder)

    
    
        
