#!/usr/bin/python3


import readgraph as rg
import networkx as nx
import argparse
import time
import itertools

# create a graph TNGraph
#G1 = snap.TNGraph.New()
#G1.AddNode(1)
#G1.AddNode(5)
#G1.AddNode(32)
#G1.AddEdge(1,5)
#G1.AddEdge(5,1)
#G1.AddEdge(5,32)

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




def std_plus_bron_kerbosch(G,k):

	if k:
		G = nx.k_core(G,k-1)

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}
	P = set(G)
	R = list()
	X = set()
	
	def expand(r,p,x,k):
		if k==0:
			yield r[:]
		if (not p and not x) or len(p) < k:
			return iter([])
		while p:
			n = p.pop()
			yield from expand(r+[n], 
				p.intersection(adj[n]),
				x.intersection(adj[n]),
				k-1)
			x.add(n)
	
	return expand(R,P,X,k)




def nx_bron_kerbosch(G,k=None):
	
	if k:
		G = nx.k_core(G,k-1)

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}

	Q = []
	cand_init = set(G)

	if not cand_init:
		return iter([])
	
	subg_init = cand_init.copy()
	
	def expand(subg, cand):
		u = max(subg, key=lambda u: len(cand & adj[u]))
		for q in cand - adj[u]:
			cand.remove(q)
			Q.append(q)
			adj_q = adj[q]
			subg_q = subg & adj_q
			if not subg_q:
				yield Q[:]
			else:
				cand_q = cand & adj_q
				if cand_q:
					yield from expand(subg_q, cand_q)
			Q.pop()

	def expandK(cand, k):
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
					yield from expandK(cand_q, k-1)
			Q.pop()

	if k is None:
		return expand(subg_init, cand_init)
	else:
		return expandK(cand_init,k)
	



def nx_plus_bron_kerbosch(G,k):
	
	G = nx.k_core(G,k-1)

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}

	Q = []
	cand_init = set(G)

	if not cand_init:
		return iter([])

	def expand(cand, k):
		
		if len(cand) < k:
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





parser = argparse.ArgumentParser(description='Arguments for enumerating maximal cliques in a graph.')
parser.add_argument('--file', '-f',
					help='Full path to the file where the graph is located.',
					required=True)
parser.add_argument('--verbose', '-v',
					dest='verbose',
					default=False,
					help='Produce verbose output',
					action='store_true')
parser.add_argument('--output', '-o',
					help='Name of output file for cliques',
					required=True)
parser.add_argument('--mode', '-m',
		    		type=str,
					help='Algorithm to be executed. One between \"standard\" (default), \"standard+\", \"nx\", \"nx+\" implementation.',default="standard")
parser.add_argument('-k',
					type=int,
					default=0,
					help='Find all cliques with size equals to k' )
parser.add_argument('--compare', '-c',
		    		help='Print all informations useful to compare a the file provided')
args = parser.parse_args()

#print(dir(snap)) # print all methods


# print('verbose=' + str(args.verbose));
verbose = True if args.verbose else False

if args.k is not None and args.k > 1:
	k = args.k
else:
	k = None

if args.file:
	G = rg.BuildNetworkxGraphFromFile(args.file,verbose)
else:
	if verbose: print('defining a new graph')
	G = nx.Graph()
	if verbose: print("adding the edges")
	G.add_edge(1,2)
	G.add_edge(2,4)

if verbose: print(f'computing all maximal cliques with {args.mode} implementaion')
start = time.time()
if args.mode == "standard":
	gen_a, gen_b = itertools.tee(std_bron_kerbosch(G,k))
elif args.mode == "nx":
	gen_a, gen_b = itertools.tee(nx_bron_kerbosch(G,k))
elif args.mode =="standard+" and k:
	gen_a, gen_b = itertools.tee(std_plus_bron_kerbosch(G,k))
elif args.mode == "nx+" and k:
	gen_a, gen_b = itertools.tee(nx_plus_bron_kerbosch(G,k))
else :
	print("algorithm unaccepted")
	exit()

clique_count = 0

for clique in gen_a:
	clique_count += 1

end = time.time()

if args.compare:
	if verbose: ('printing all maximal cliques')
	with open(args.output, 'w') as f:
		for clique in gen_b:
			f.write("%s\n" % clique.sort())
else:
	if verbose: print('printing graph_name, #nodes, #edges, #cliques, time')
	with open(args.output, 'a') as f:
		f.write("%s;%d;%d;%d;%f\n" % (G.graph['name'],G.number_of_nodes(),G.number_of_edges(),clique_count,end-start))

if args.compare:
	var = "maximal" if not k else str(k)
	with open(args.compare, 'a') as f:
		print(f"### {args.mode} implmentation: seconds for enumerating %d {var}-cliques: %f" % (clique_count,end-start), file=f)
	print(f"### {args.mode} implmentation: seconds for enumerating %d {var}-cliques: %f" % (clique_count,end-start))

if verbose: print("find-cliques.py: End of computation")

