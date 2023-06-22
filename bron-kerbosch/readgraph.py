import re # regular expressions
import networkx as nx


# def BuildSnapGraphFromFile(file_name, verbose=True):
#     if verbose: print("BuildGraphFromFile()")
#     if verbose: print("Building Snap graph from file %s..." % file_name)
#     G1 = snap.TUNGraph.New()
#     stack = set()
#     lines = [line.strip() for line in open(file_name)]
#     for line in lines:
#         l = re.split('\t| ',line)
#         if(int(l[0]) not in stack):
#            G1.AddNode(int(l[0]))
#            stack.add(int(l[0]))
#         if( int(l[1]) not in stack):
#            G1.AddNode(int(l[1]))
#            stack.add(int(l[1]))
#         G1.AddEdge(int(l[0]),int(l[1]))
#         G1.AddEdge(int(l[1]),int(l[0]))
#     return G1

# old function. 
def BuildNetworkxGraphFromFile_old_version(file_name, verbose=True):
    if verbose: print("BuildNetworkxGraphFromFile()")
    import re # regular expressions
    if verbose: print("Building Networkx graph from file %s..." % file_name)
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


def BuildNetworkxGraphFromFile(file_name, verbose=True):
    if verbose: print("BuildNetworkxGraphFromFile()")
    import re # regular expressions
    if verbose: print("Building Networkx graph from file %s..." % file_name)
    G1 = nx.Graph() # undirected graph
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = re.split('\t| ',line)
        G1.add_edge(int(l[0]),int(l[1]))
    return G1