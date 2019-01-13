from habanero import Crossref
from pprint import pprint
import csv
import json
import uuid

import name_norm
import numpy
from collections import Counter
import itertools
from multiprocessing.dummy import Pool as ThreadPool 



def safeGetTitle(x):
    return x[0] if x else None

def nameAliasToFilename(name_alias):
    return name_norm.name_normalise(name_alias).replace(" ","_")+".json"

dumped_query_path = './publikacjeDir_dump/'

def dumpQueryDataLocal(obj, query_name_alias):
    with open(dumped_query_path+nameAliasToFilename(query_name_alias),"w") as jsonfile:
            json.dump(obj, jsonfile)

def getQueryDataLocal(query_name_alias):
    obj = None
    try:
        with open(dumped_query_path+nameAliasToFilename(query_name_alias),"r") as jsonfile:
            obj = json.load(jsonfile)
        return obj
    except EnvironmentError: 
        print("missed file")
    return None

def getQueryDataRemote(query_name_alias, cr):
    print("ask remote")
    res = cr.works(query_author = query_name_alias, limit=25)
    res['custom_name_alias'] = query_name_alias
    dumpQueryDataLocal(res, query_name_alias)
    return res
        
def getQueryData(query_name_alias, cr):
    obj = getQueryDataLocal(query_name_alias)
    if obj != None:
        return obj
    else:
        return getQueryDataRemote(query_name_alias, cr)
    
def getManCoworkers(name_alias, cr):
    obj = None
    obj = getQueryData(name_alias, cr)
    
    normalized_name = name_norm.name_normalise(name_alias)
    
    cowrs = Counter()
    
    
    for i in obj['message']['items']:
        names_in_authors = set()
        
        for aut in i ['author']:

            aut_name=""
            if 'family' in aut:
                aut_name = aut_name + aut['family'] 
            if 'given' in aut:
                aut_name = " ".join([aut_name,aut['given']])
            if 'family' not in aut or 'given' not in aut:
                print(aut)
                aut_name = " ".join(aut_name.split()[::-1])
            
            if aut_name != "":
                aut_name = name_norm.name_normalise(aut_name)
                names_in_authors.add(aut_name)
                #                print("aut 4 com %s"%aut_name)
        
        if normalized_name in names_in_authors:
            cowrs.update(names_in_authors)
            
    
    return cowrs
    
    

def load_alias_list():
    with open('inventors_w_aliases.csv',"r") as csvfile:
        csv_inventors = csv.reader(csvfile, delimiter=',')
        data  = list(csv_inventors)

    aliases = list(set([x[1] for x in data[2:]]))
    aliases.sort()
    return aliases




def save_all_this_sit():
    """
    generuje csv, gdzie w kazdrym rzedzie jest imie, imie wspoltworcy, i liczba mowiaca o ilosci wspolnych punlikacji
    """
    aliases = load_alias_list()
    net = dict();
    for c,i in enumerate(aliases):
        net[i] = getManCoworkers(i,None)
        if c > 100:
            break
    
    with open('publication_coworking.csv',"w") as csvfile:
        writer = csv.writer(csvfile,)
        writer.writerow(("person_name_alias","coworker_name_alias","common_publications_count"))

        for name_alias, counter in sorted(list(net.items())):
            for coworker_name_alias in counter:
                writer.writerow((name_alias,coworker_name_alias,counter[coworker_name_alias]))





def parallel_task(data):
    (id,alias,cr) = data
    print("processing alias=%s with id=%d"%(alias,id))
    pprint(getManCoworkers(alias,cr))


def download_all_this_things_in_parallalale():
    aliases = load_alias_list()
    pool = ThreadPool(2) 
    pool.map(parallel_task,  [[id,alias,cr] for id, alias in enumerate(aliases)])
    
def download_all_this_things():
    load_alias_list()
    for i in [(id,alias,cr) for id,alias in enumerate(aliases)]:
        print(parallel_task(i))
    
    
cr = Crossref(mailto = "jedr.ka@gmail.com")
#save_all_this_sit()
download_all_this_things_in_parallalale()
exit(0)
    
    
