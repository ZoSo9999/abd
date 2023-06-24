import networkx as nx
from pprint import pprint


def std_bron_kerbosch(G,k=None):

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
		u = max(p.union(x), key=lambda u: len(p & adj[u])) if p.union(x) else None
		adj_u = adj[u] if u else set()
		for n in p - adj_u:
			yield from expand(r+[n], 
				p.intersection(adj[n]),
				x.intersection(adj[n]))
			p.remove(n)
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
	G1 = nx.karate_club_graph()
	k = 2
	l1 = list(std_bron_kerbosch(G1))
	# l2 = list(std_bron_kerbosch(G))
	l2 = list(nx.find_cliques(G1))
	pprint(l1)
	print(len(l1))
	pprint(l2)
	print(len(l2))


