import networkx as nx
from pprint import pprint


def std_bron_kerbosch(G,k):

	if k:
		G = nx.k_core(G,k-1)

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}
	P = set(G)
	R = list()
	X = set()
	
	def expand(r,p,x):
		if not p and not x:
			yield r[:]
		while p:
			n = p.pop()
			yield from expand(r+[n], 
				p.intersection(adj[n]),
				x.intersection(adj[n]))
			x.add(n)
	
	def expandK(r,p,x,k):
		if k==0:
			yield r[:]
		if not p and not x:
			return iter([])
		while p:
			n = p.pop()
			yield from expandK(r+[n], 
				p.intersection(adj[n]),
				x.intersection(adj[n]),
				k-1)
			x.add(n)
	
	if k is None:
		return expand(R,P,X)
	else:
		return expandK(R,P,X,k)
	


if __name__ == "__main__":
	G = nx.Graph()
	G.add_nodes_from([1,2,3,4])
	G.add_edges_from([(1, 2), (2, 3), (3,4)])
	pprint(list(G.nodes))
	pprint(list(G.edges))
	k = 3
	l2 = list(std_bron_kerbosch(G,k))
	# l2 = list(nx.find_cliques(G))
	pprint(l2)
	print(len(l2))


