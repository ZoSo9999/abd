# cand contiene i nodi candidati e serve per il ciclo for
# subg serve per verificare che il nodo q scelto abbia altri nodi adiacenti da inserire nella clique
# dopo lo yield e il pop può succedere che subg sia vuoto e cand-adj[pivot] invece non lo sia e quindi il ciclo prosegue

# Non posso eseguire quanto richiesto con Tomita, si pensi ad una clique di dimensione 5 e un k=4, non otterrò mai tutte le combinazioni

from pprint import pprint
import networkx as nx


def std_bron_kerbosch(G,k):

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}
	P = set(G)
	R = set()
	X = set()
	
	def expand(R,P,X):
		if not P and not X:
			yield R[:]
		for n in P:
			print("cazzo")
			yield from expand(R.add(n), P & adj[n], X & adj[n])
			X.add(n)
			P.remove(n)
	
	def expandK(R,P,X,k):
		if k==0:
			yield R[:]
		for n in P:
			yield from expandK(R.add(n), P & adj[n], X & adj[n], k-1)
			X.add(n)
			P.remove(n)
	
	if k is None:
		return expand(R,P,X)
	else:
		return expandK(R,P,X,k)

def enum_k_clique1(G,k):

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}

	Q = []
	cand_init = set(G)

	if not cand_init:
		return iter([])
	
	def expand(cand, k):

		for q in cand:
			last = Q[-1] if Q else -1
			if last > q:
				continue
			Q.append(q)
			if k == 1:
				yield Q[:]
			else:
				adj_q = adj[q]
				cand_q = cand & adj_q
				if cand_q:
					yield from expand(cand_q, k-1)
			Q.pop()

	return expand(cand_init, k)




def enum_k_clique2(G,k):

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}

	Q = []
	cand_init = set(G)

	if not cand_init:
		return iter([])

	def expand(cand, k):
		
		if len(Q)+len(cand) < k:
			return iter([])
		for q in cand:
			last = Q[-1] if Q else -1
			if last > q:
				continue
			Q.append(q)
			if k == 1:
				yield Q[:]
			else:
				adj_q = adj[q]
				cand_q = cand & adj_q
				if cand_q:
					yield from expand(cand_q, k-1)
			Q.pop()

	return expand(cand_init, k)


if __name__ == "__main__":
	G = nx.karate_club_graph()
	k = 4
	#l1 = list(enum_k_clique2(G,k))
	l2 = list(nx.find_cliques(G))
	pprint(l2)
	print(len(l2))
	l3 = list(std_bron_kerbosch(G,None))
	pprint(l3)
	print(len(l3))