import networkx as nx

k = 10
G = nx.fast_gnp_random_graph(20,0.7,3)
G1 = nx.k_core(G,k-1)
