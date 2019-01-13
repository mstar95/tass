import networkx as nx
import csv
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,12))
ax = plt.subplot(111)

def load_coworkers():
    with open('publication_coworking.csv',"r") as csvfile:
        csv_coworkers = csv.reader(csvfile, delimiter=',')
        data  = list(csv_coworkers)
    return data[1:]


data = load_coworkers()


G=nx.Graph()
G.add_weighted_edges_from(data)

pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=10, node_color='yellow', font_size=8, font_weight='bold')

plt.tight_layout()
plt.savefig("Graph.png", format="PNG")