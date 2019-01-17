import csv


with open('inventors_w_aliases.csv',"r") as csvfile:
    csv_inventors = csv.reader(csvfile, delimiter=',')
    data  = list(csv_inventors)
    aliases = list(set([x[1] for x in data[2:]]))

with open('ludzie_liczba_patentow_normalized.csv',"r") as csvfile:
    csv_patents = csv.reader(csvfile, delimiter=',')
    patents = list(csv_patents)

with open('publication_coworking.csv',"r") as csvfile:
    csv_coworking = csv.reader(csvfile, delimiter=',')
    coworking = list(csv_coworking)


aliases.sort()

result = []

for alias in aliases:
    res = list(filter(lambda p: p[0] == alias, patents))
    if not res:
        continue
    patentNr = res[0][1]
    coworkers = list(filter(lambda p: p[0] == alias, coworking))
    finalValue = 0
    coworkersCounter = 0
    for coworker in coworkers:
        name = coworker[1]
        if name == alias:
            continue
        res = list(filter(lambda p: p[0] == name, patents))
        if not res:
            value = 0
        else:
            value = int(coworker[2]) * int(res[0][1])
        finalValue = finalValue + value
        coworkersCounter = coworkersCounter + int(coworker[2])
    if coworkersCounter != 0:
        coworkersPatents = finalValue / coworkersCounter
        average = 0
        if coworkersPatents != 0.0:
            average = int(patentNr) / coworkersPatents
        result.append((alias, patentNr, coworkersPatents, average))
        
with open('roznice_w_patentach_wszystkie.csv',"w") as csvfile:
    writer = csv.writer(csvfile,)
    writer.writerow(("inventor","patents","coworkers_patents", "patents/coworkers_patents"))
    subs = result
    writer.writerows(subs)
