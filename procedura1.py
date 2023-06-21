import networkx as nx
import matplotlib.pyplot as plt
import itertools

k = 10
G = nx.fast_gnp_random_graph(35,0.7,1)
print(G)
# print(list(G.nodes))
# print(list(G.edges))

# for n in G:
#     print(G.degree[n])

# core = nx.core_number(G)
# print(core)

# filtered_core = {key: value for key, value in core.items() if value > k-2}
# print(filtered_core)

# G1 = nx.subgraph(G,filtered_core)
# print(G1)

#nx.draw(G, with_labels=True)
#plt.show()

G1 = nx.k_core(G,k-1)
print(G1)

filtered_clique = list(filter(lambda x: len(x) >= k , nx.find_cliques(G1)))
print(filtered_clique)


def subsets(list):
    if list == []:
        return [[]]
    x = subsets(list[1:])
    return x + [[list[0]] + y for y in x]
 
def subsets_of_given_size(list, n):
    return [x for x in subsets(list) if len(x)==n]

for list in filtered_clique:
    k_clique = subsets_of_given_size(list,k)
    print(k_clique)