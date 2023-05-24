import networkx as nx
import matplotlib.pyplot as plt

k = 10
G = nx.fast_gnp_random_graph(20,0.7)
# print(list(G.nodes))
# print(list(G.edges))

# for n in G:
#     print(G.degree[n])

core = nx.core_number(G)
print(core)

filtered_core = {key: value for key, value in core.items() if value > k-2}
print(filtered_core)

#nx.draw(G, with_labels=True)
#plt.show()

maximal_cliques = list(nx.find_cliques(G))
print(maximal_cliques[0])