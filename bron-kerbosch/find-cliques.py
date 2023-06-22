#!/usr/bin/python3


# ATTENTION: for the following import execute "pip3 install snap-stanford" and not "pip3 install snap"
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

def std_bron_kerbosch(G,k):

	if len(G) == 0:
		return iter([])

	adj = {u: {v for v in G[u] if v != u} for u in G}
	P = set(G)
	R = set()
	X = set()
	
	def expand(R,P,X):
		if not P and not X:
			return R
	for n in P:
		expand(R.add(n),P & adj[n], X & adj[n])
		X.add(n)
		P.remove(n)
	
	def expandK(R,P,X,k):
		if k==0:
			return R
	for n in P:
		expandK(R.add(n),P & adj[n], X & adj[n],k-1)
		X.add(n)
		P.remove(n)
	
	if k is None:
		return expand(R,P,X)
	else:
		return expandK(R,P,X,k)



def nx_bron_kerbosch(G,k):

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
					yield from expand(cand_q, k-1)
			Q.pop()

	if k is None:
		return expand(subg_init, cand_init)
	else:
		return expandK(cand_init,k)

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
					help='Name of output file for cliques')
parser.add_argument('--mode',
					help='Algorithm to be executed. One between \"standard\" (default) or \"nx\" implementation.',default="standard")
parser.add_argument('-k',
					type=int,
					default=0,
					help='Find all cliques with size equals to k' )
args = parser.parse_args()

#print(dir(snap)) # print all methods


# print('verbose=' + str(args.verbose));

if args.verbose: verbose = True
if args.k is not None and args.k > 1:
	k = args.k
else:
	k = None

if args.file != "":
	G = rg.BuildNetworkxGraphFromFile(args.file,verbose)
else:
	if verbose: print('defining a new graph')
	G = nx.Graph()
	if verbose: print("adding the edges")
	G.add_edge(1,2)
	G.add_edge(2,4)

if verbose: print('computing all maximal cliques with networkx')
start = time.time()
if args.mode == "standard":
	gen_a, gen_b = itertools.tee()
else:
	gen_a, gen_b = itertools.tee(nx_bron_kerbosch(G,k))

clique_count = 0

for clique in gen_a:
	clique_count += 1

end = time.time()

if args.output != "":
	f = open(args.output, 'w')
	for clique in gen_b:
		f.write("%s\n" % clique)
else:
	if args.verbose: 
		print('printing all maximal cliques')
	for clique in gen_b:
		clique_count += 1
		print(clique)

if args.mode == "standard":
	print(" MAXIMAL: seconds for enumerating %d cliques: %f" % (clique_count,end-start))
else:
	print(" NX implementation: seconds for enumerating %d %d-cliques: %f" % (clique_count,k,end-start))

if args.verbose: print("find-cliques.py: End of computation")

