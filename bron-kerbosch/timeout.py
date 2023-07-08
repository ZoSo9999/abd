import networkx as nx
import readgraph as rg
import argparse

parser = argparse.ArgumentParser(description='Arguments for executions in timeout.')
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
					help='One between \"all\" and \"single\".',
					required=True)
parser.add_argument('--time', '-t',
					help='Timeout time',
					required=True)
args = parser.parse_args()

G = rg.BuildNetworkxGraphFromFile(args.file)

if args.verbose: print(f"{G.graph['name']}: {args.time} seconds timeout exceeded")

if args.mode == 'single':
	with open(args.output, 'a') as f:
		f.write("%s;%d;%d;%d;%f\n" % (G.graph['name'],G.number_of_nodes(),G.number_of_edges(),0,int(args.time)))

elif args.mode == 'all':
	with open(args.output, 'a') as f:
		f.write("%d;%f" % (0,int(args.time)))