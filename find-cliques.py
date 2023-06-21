#!/usr/bin/python3


# ATTENTION: for the following import execute "pip3 install snap-stanford" and not "pip3 install snap"
# import snap
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
                    help='Algorithm to be executed. One between \"Iterative\" (default) or \"Recursive\".',default="Iterative")

args = parser.parse_args()

#print(dir(snap)) # print all methods


# print('verbose=' + str(args.verbose));

def BuildSnapGraphFromFile(file_name):
    if args.verbose: print("BuildGraphFromFile()")
    import re # regular expressions
    if args.verbose: print("Building Snap graph from file %s..." % file_name)
    G1 = snap.TUNGraph.New()
    #G1 = snap.TNGraph.New()
    stack =set()
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = re.split('\t| ',line)
        if(int(l[0]) not in stack):
           G1.AddNode(int(l[0]))
           stack.add(int(l[0]))
        if( int(l[1]) not in stack):
           G1.AddNode(int(l[1]))
           stack.add(int(l[1]))
        G1.AddEdge(int(l[0]),int(l[1]))
        G1.AddEdge(int(l[1]),int(l[0]))
    return G1

# old function. 
def BuildNetworkxGraphFromFile_old_version(file_name):
    if args.verbose: print("BuildNetworkxGraphFromFile()")
    import re # regular expressions
    if args.verbose: print("Building Networkx graph from file %s..." % file_name)
    G1 = nx.Graph()
    stack =set()
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = re.split('\t| ',line)
        if(int(l[0]) not in stack):  
           G1.add_node(int(l[0])) # nonsense, non existent nodes are automatically added
           stack.add(int(l[0]))
        if( int(l[1]) not in stack):
           G1.add_node(int(l[1]))
           stack.add(int(l[1]))
        G1.add_edge(int(l[0]),int(l[1]))
        G1.add_edge(int(l[1]),int(l[0])) # nonsense, adding two times the same edge
    return G1


def BuildNetworkxGraphFromFile(file_name):
    if args.verbose: print("BuildNetworkxGraphFromFile()")
    import re # regular expressions
    if args.verbose: print("Building Networkx graph from file %s..." % file_name)
    G1 = nx.Graph() # undirected graph
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = re.split('\t| ',line)
        G1.add_edge(int(l[0]),int(l[1]))
    return G1

if args.file != "":
	G = BuildNetworkxGraphFromFile(args.file)
else:
	if args.verbose: print('defining a new graph')
	G = nx.Graph()
	if args.verbose: print("adding the edges")
	G.add_edge(1,2)
	G.add_edge(2,4)

if args.verbose: print('computing all maximal cliques with networkx')
start = time.time()
if args.mode == "Iterative":
	gen_a, gen_b = itertools.tee(nx.find_cliques(G))
else:
	gen_a, gen_b = itertools.tee(nx.find_cliques_recursive(G))

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

if args.mode == "Iterative":
	print(" ITERATIVE: seconds for enumerating %d cliques: %f" % (clique_count,end-start))
else:
	print(" RECURSIVE: seconds for enumerating %d cliques: %f" % (clique_count,end-start))

if args.verbose: print("find-cliques.py: End of computation")

