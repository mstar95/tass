import name_norm
from pprint import pprint,pformat
from collections import Counter
import csv

with open('ludzie_liczba_patentow.csv',"r") as csvfile:
        csv_inventors = csv.reader(csvfile, delimiter=',')
        header = next(csv_inventors)
        data  = list(csv_inventors)


cnt = Counter()
for man in data:
    print(man)
    name = name_norm.inventor_name_normalise(man[0])
    cnt[name]+=int(man[1])
    
pprint(cnt)

with open('ludzie_liczba_patentow_normalized.csv',"w") as csvfile:
    writer = csv.writer(csvfile,)
    writer.writerow(header)

    for name in cnt:
        writer.writerow((name,cnt[name]))
