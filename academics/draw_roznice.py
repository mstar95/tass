import matplotlib.pyplot as plt
import csv
import numpy as np

with open('roznice_w_patentach_wszystkie.csv',"r") as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',')
    data = list(csv_data)[1:]

averages = [float(x[3]) for x in data]
averages.sort()
print(max(averages))
percentiles = [np.percentile(averages, x) for x in range(0,101)] 

print(percentiles)

# lists = sorted(res.items()) # sorted by key, return a list of tuples

# x, y = zip(*lists) # unpack a list of pairs into two tuples

# print(max(x))
# print(max(y))
plt.plot([x for x in range(0,101)] , percentiles)

plt.savefig('roznice.png')
