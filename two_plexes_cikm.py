#!/usr/bin/python

#from pyspark import SparkConf, SparkContext 
from collections import defaultdict
import collections
import networkx as nx
import os.path
from operator import add
import sys
import time
import datetime
import argparse
import itertools

parser = argparse.ArgumentParser(description='Arguments for enumerating 2-plexes in a graph.')
#parser.add_argument('--k',type=int,
#                    help='How many non neighbors a node is allowed to have.',default=5)
parser.add_argument('--file', '-f',
					required=True,
                    help='path to the file where the graph is located.',
                    default="")
parser.add_argument('--output', '-o',
                    help='name of output file for printed 2-plexes. Default value is "output_file"',
                    default="output_file")
parser.add_argument('--minsize', '-ms',
					type=int,
                    help='the minimum size of the 2-plexes to be produced',
                    default=0)
parser.add_argument('--type',
                    help='''What type of 2-plexes has to be produced. Can be one of 
                    the following: "all", "connected". Default value is "all"''',
                    default="all")
parser.add_argument('--architecture', '-a',
                    help='''What type of architecture to use. Can be one of 
                    the following: "local", "spark". Default value is "local"''',
                    default="local")
parser.add_argument('--algo', 
                    help='''What type of algorithm to use. Can be one of 
                    the following: "basic", "comp_by_comp". Default value is "basic"''',
                    default="basic")
parser.add_argument('--verbose', '-v',
                    dest='verbose', 
                    default=False, 
                    help='Produce verbose output',
                    action='store_true')


args = parser.parse_args()

if args.architecture == "spark":
	print("loading pyspark")
	from pyspark import SparkConf, SparkContext 


##################################################################################

# Calcola i due plessi e ritorna il numero dei 2-plessi trovati.
# Prende in input un'oggetto x che ha in x[0] una node-list (che comunque non
# viene consultata) e in x[1] una edge-list (coppie di nodi) dove ogni nodo e' una stringa.
#
def two_plexes_basic(x):
	
	# if args.verbose: print("%s: starting two_plexes_basic()" % (sys.argv[0]))

	#x[0] = x[0].split(",")
	#print x
	#boundary = list(nx.node_boundary(G,x))
  	#kernel = x+boundary
  	#print x[0]
  	#print x[1]

	# preparo una lista vuota per i 2-plessi
	#
	twoplex = []
	numberOf2plex = 0   # futuro output
	
	# costruisco il grafo a partire dalla lista degli archi
    # converto i nodi in stringhe
    # x[1] = ["1 2", ... "2 3", "3 4"...]
	#
	G = nx.parse_edgelist(x[1], nodetype = str)
	# if args.verbose: print("%s:  snap graph built" % (sys.argv[0]))
	
	# Definition of lambda function "compare" (al momento non la usa nessuno)
	#
	compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

	# Construct the dual graph of G
	#
	dualG = dual(G)
	# if args.verbose: print("%s:  dual graph built" % (sys.argv[0]))
	
    # Costruisco il duale del grafo dei conflitti
    #
	dualConflictG = dualConflictGraph(dualG,G)
	# if args.verbose: print("%s:  dual of conflict graph built" % (sys.argv[0]))

	# DEBUG
	#
	# print("Dual of conflict graph") 
	# print(dualConflictG.edges()) 

	# Cancello il duale del grafo originale
    #
	dualG.clear()
	
	#dualConflictG = dual(conflictG) # non serve perche' e' gia' il duale
	#print dualConflictG.nodes() # DEBUG
	
	# Preparo una lista vuota di 2-plessi
	#
	plex = []

	# Metto nella lista dei 2-plessi le clique del duale del conflict-graph
	# cioe' i maximal independent set del grafo dei conflitti (gli insiemi 
    # massimali di nodi compatibili).
	#
	# if args.verbose: print("%s:  computing cliques of dual of conflict graph" % (sys.argv[0]))
	plex = list(nx.find_cliques(dualConflictG))  # find (maximal) cliques
	# if args.verbose: print("%s:  computed cliques of dual of conflict graph" % (sys.argv[0]))
	# print("============= independent sets of conflict graph ================")
	# print(plex)
	# print("=================================================================")

	#if args.verbose: print("%s:   found %s cliques" % (sys.argv[0],str(len(plex))))

	for pl in plex:
		#if args.verbose: print("%s:   considering clique %s" % (sys.argv[0],pl))

		# Costruisco correctPl che sara' il 2-plesso espresso tramite una 
		# lista di nodi di G a partire da pl che e' invece la lista dei 
		# nodi del conflict graph.
		#
		correctPl = [] 
		for n in pl:
			#print n
			nod = n.split("-")
			#print "NOD"+str(nod)
			correctPl.append(int(nod[0]))
			if len(nod) > 1:
				correctPl.append(int(nod[1]))

		correctPl.sort()
		#print("CorrectPL    "+str(correctPl))
		#correctPlNew = list(set(correctPl))
		#correctPlNew.sort()
		#print("correctPlNew "+str(correctPlNew))
		#print correctPlNew
		#print type(correctPl[0])
		#print "---------------------------------"+str(correctPlNew)
		#tmppl = [str(correctPlNew[0])]   # ATTENZIONE: NESSUNO LO USA?
		
		#print tmppl
		#checkDuplicate = complete_two(tmppl,pl,G)
		#print "Complete 1  "+str(checkDuplicate)
		
		#checkDuplicate2 = complete_tree(checkDuplicate,cliques)
		
		#print "Complete 2  "+str(checkDuplicate2)
		#print "c      "+str(c)
		#print "c      "+str(c)
		#if compare(checkDuplicate2,x[0]):
		#print "compare"

		#isMaximal = 1
		
		if args.type == "connected":
			# Non-connected maximal 2-plexes are non-edges of G that are not 
			# contained into other 2-plexes. To filter them out it is sufficient
			# to filter out all candidates that are non-edges of G
			#
			if len(pl) == 1: # this plex is a single node of the conflict graph, hence 
			                 # it is either an edge or a non-edge of G
				nodes = pl[0].split("-")
				# print("nodes[0] = "+nodes[0])
				# print("nodes[1] = "+nodes[1])
				if not G.has_edge(nodes[0],nodes[1]): # this is a non-edge
					continue # discard this 2-plex because it is not connected
			
		isMaximal = checkMaximality(pl,dualConflictG)
		if isMaximal == 0:
			continue  # discard this 2-plex because it is not maximal

		if len(correctPl) >= args.minsize:
			numberOf2plex = numberOf2plex+1	
			output_file.write("%s\n" % str(correctPl))
			#print(correctPlNew)
			#twoplex.append(correctPlNew)


	# Cancella il conflict-graphclique 
	#
	dualConflictG.clear()
	
	return numberOf2plex



##################################################################################

# Calcola i due plessi e ritorna il numero dei 2-plessi trovati.
# Prende in input un'oggetto x che ha in x[0] una node-list (che comunque non
# viene consultata) e in x[1] una edge-list (coppie di nodi) dove ogni nodo e' una stringa.
#
def two_plexes_comp_by_comp(x):
	
	#x[0] = x[0].split(",")
	#print x
	#boundary = list(nx.node_boundary(G,x))
  	#kernel = x+boundary
  	#print x[0]
  	#print x[1]

	# preparo una lista vuota per i 2-plessi
	#
	twoplex = []
	numberOf2plex = 0   # futuro output
	
	# costruisco il grafo a partire dalla lista degli archi
    # converto i nodi in stringhe
    # x[1] = ["1 2", ... "2 3", "3 4"...]
	#
	G = nx.parse_edgelist(x[1], nodetype = str)

	# I 2-plessi massimali di G si dividono in 2-plessi massimali connessi e 
	# 2-plessi massimali non-connessi.
	# 	I 2-plessi massimali connessi possono avere dimensione 1, 2, o maggiore di due.
	# 		I 2-plessi massimali connessi di dimensione 1 sono nodi isolati (facili da 
	#		trovare: sono le componenti connesse di G di dimensione 1).
	# 		I 2-plessi massimali connessi di dimensione 2 sono archi che non partecipano 
	#		a 2-plessi piu' grandi, cioe' archi isolati di G (facili da trovare: sono le 
	#		componenti connesse di G di dimensione 2).
	#		I 2-plessi connessi di dimensione > 2 sono quelli che cercheremo con il nostro 
	#		algoritmo.
	# 	I 2-plessi massimali non-connessi non possono avere piu' di due nodi, quindi sono 
	#	non-archi che non partecipano a 2-plessi piu' grandi. 
	#	I 2-plessi massimali non-connessi si dividono in 2-plessi massimali non-connessi che
	#	spannano una sola componente connessa di G e 2-plessi massimali non-connessi che
	#	spannano due componenti connesse di G. 
	#		I 2-plessi massimali non-connessi che spannano due componenti connesse di G
	#		sono facili da trovare. Infatti, considera un non-arco (u,v) tra due componenti 
	#		connesse di G. {u,v} e' sicuramente un 2-plesso. Dimostriamo che e' sempre un 2-plesso 
	#		massimale. Supponiamo per assurdo che non lo sia. Allora un altro nodo w deve 
	#		appartenere al 2-plesso contenente {u,v}. Ma u e v hanno gia' un non-arco. Dunque w
	# 		deve essere collegato sia a u che a v, contraddicendo il fatto che u e v 
	#		appartengano a due componenti connesse diverse. Dunque ogni coppia di nodi {u,v} 
	#		appartenenti a due componenti connesse diverse e' un 2-plesso massimale non-connesso. 
	#		Rimangono i 2-plessi massimali non-connessi che spannano una sola componente connessa.
	#		Questi 2-plessi sono formati da non-archi (u,v) che hanno la proprieta' che non esiste
	#		alcun vicino comune a u e v. 
	#
	#	La strategia di ricerca e' dunque la seguente: con un calcolo delle componenti connesse
	#	di G siamo in grado di identificare tutti i 2-plessi massimali connessi di dimensione
	#   1 e 2. Inoltre siamo in grado di produrre (se richiesto) tutti i 2-plessi massimali 
	#	non connessi di dimensione 2 che spannano piu' di una componente connessa.
	#	Rimangono da trovare i 2-plessi massimali connessi di dimensione > 2 (che, essendo connessi,
	#	sono ovviamente contenuti nella stessa componente connessa) e i 2-plessi massimali non-connessi 
	#	di dimensione 2 e contenuti in una sola componente connessa. Questi due tipi di 2-plessi li
	#	cerchiamo lanciando la procedura di ricerca su ogni componente connessa separatamente.

	numberOf2plexes = 0

	number_of_components = nx.number_connected_components(G)
	#print("Number of connected components = %d" % number_of_components)

	if number_of_components == 1:
		components = []
		components.append(G)
	else:
		components = list(nx.connected_component_subgraphs(G))

	for comp in components:
		comp_size = comp.number_of_nodes()
		# print("componente connessa di dimensione %d" % comp_size)
		if comp_size == 1: 			# trovato un 2-plesso massimale connesso di dim. 1
			# print("2-plesso massimale (connesso) con un solo nodo")
			if args.minsize <= 1:	# l'articolo interessa l'utente
				numberOf2plexes = numberOf2plexes+1
				output_file.write("%s\n" % str(comp.nodes()))
				# print("[%s]" % comp.nodes()[0])
		elif comp_size == 2:		# trovato un 2-plesso massimale connesso di dim. 2
			# print("2-plesso massimale (connesso) con due nodi (un arco isolato)")
			if args.minsize <= 2:	# l'articolo interessa l'utente
				numberOf2plexes = numberOf2plexes+1
				nodeset = comp.nodes()
				nodeset.sort()
				output_file.write("[%s, %s]\n" % (nodeset[0],nodeset[1]))
				# print("[%s, %s]" % (nodeset[0],nodeset[1]))
		elif comp_size == 3:		# e' sempre un 2-plesso massimale connesso
			# print("2-plesso massimale (connesso) con due nodi (un arco isolato)")
			if args.minsize <= 3:	# l'articolo interessa l'utente
				numberOf2plexes = numberOf2plexes+1
				nodeset = comp.nodes()
				nodeset.sort()
				output_file.write("[%s, %s, %s]\n" % (nodeset[0],nodeset[1]),nodeset[2])
				# print("[%s, %s]" % (nodeset[0],nodeset[1],nodeset[2]))
		else:
			# print("componente con piu' di tre nodi")
			numberOf2plexes = numberOf2plexes + two_plexes_of_component(comp)
		
	if args.type == "all":	# the user also asked for non-connected 2-plexes
		for pair in itertools.combinations(components, 2): # this takes all pairs in order
			#(*pair)
			for n1 in pair[0].nodes():
				for n2 in pair[1].nodes():
					numberOf2plexes = numberOf2plexes+1
					output_file.write("[%s, %s]\n" % (n1,n2))
					#print("[%s, %s]" % (n1,n2))
			# comp1_size = pair[0].number_of_nodes()				
			# comp2_size = pair[1].number_of_nodes()				
			# print("found a pair %d %d" % (comp1_size,comp2_size))
		
	# numberOf2plexes = numberOf2plexes + two_plex_of_component(G)	
	return numberOf2plexes

# two_plexes_of_component(G)
# Returns the number of 2-plexes of the connected component G and prints them
# in the output file.
# It is assumed that:
# 1) G is connected. Actually, we only use that it has no isolated node
# 2) G has at least 4 nodes, as otherwise the whole component is trivially a 2-plex.

def two_plexes_of_component(G):

	#bicomponents = list(nx.biconnected_components(G))
	#number_of_bicomps = len(bicomponents)
	# if args.verbose: print("number of bicomps = %d" % number_of_bicomps)

	numberOf2plex = 0

	# Definition of lambda function "compare" (al momento non la usa nessuno)
	#
	# compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

	# Construct the dual graph of G
	#
	dualG = dual(G)

    # We build the dual of the conflict graph.
    #
	dualConflictG = dualConflictGraph(dualG,G)

	# DEBUG
	#
	# print("Dual of conflict graph") 
	# print(dualConflictG.edges()) 

	# Cancello il duale del grafo originale
    #
	dualG.clear()
	
	#dualConflictG = dual(conflictG) # non serve perche' e' gia' il duale
	#print dualConflictG.nodes() # DEBUG
	
	# Preparo una lista vuota di clicche
	#
	cliques = []

	# Metto nella lista "cliques" le clique del duale del conflict-graph
	# cioe' i maximal independent set del grafo dei conflitti (gli insiemi 
    # massimali di nodi compatibili).
	#
	cliques = list(nx.find_cliques(dualConflictG))  # find (maximal) cliques
	# print("============= independent sets of conflict graph ================")
	# print(cliques)
	# print("=================================================================")

	#print "Lunghezza plessi trovati : "+str(len(cliques))

	for candidate in cliques:

		# Observe that the clique "candidate" cannot be composed of a single node "N" 
		# that comes from a node "n" of G (and not from an edge of G). In fact, 
		# this would imply that "N" is an isolated node of the graph "dualConflictG". 
		# This, in turn, implies that "N" is connected to all other nodes in the
		# (primal) conflict-graph. However, the fact that "N" is connected to all
		# those nodes (of the conflict-graph) that come from nodes of G implies that
		# "n" has non-edges towards all other nodes of G. That is "n" is an isolated
		# vertex of "G", contradicting the hypothesis that "G" is connected. 
		# 
		#
		if args.type == "connected":
			# The user asked to filter out non-connected maximal 2-plexes.
			# Non-connected maximal 2-plexes are non-edges of G that are not 
			# contained into other 2-plexes. To filter them out it is sufficient
			# to filter out all "candidates" maximal cliques that correspond to
			# non-edges of G.
			#
			if len(candidate) == 1: # this clique of the graph "dualConflictG" is  
			                        # composed by a single node of the conflict graph, 
			                        # For what we said above, it is a non-edge of "G". 
									# We can discard it because it is not connected.
									# Maximality test is not needed because "candidate"
									# has no nodes coming from single nodes of "G"
				continue

		# Costruisco "candidate_two_plex" che sara' il 2-plesso espresso tramite una 
		# lista di nodi di G a partire da "candidate" che e' invece la lista dei 
		# nodi di una clique massimale del duale del conflict graph.
		#
		candidate_two_plex = [] 
		for n in candidate:
			# print n
			nod = n.split("-")
			# print "NOD"+str(nod)
			candidate_two_plex.append(int(nod[0]))
			if len(nod) > 1:
				candidate_two_plex.append(int(nod[1]))

		if len(candidate_two_plex) < args.minsize:
			continue # discard this two-plex (maximal or not) because it is too small 

		#print("candidate_two_plex    "+str(candidate_two_plex))
		#candidate_two_plexNew = list(set(candidate_two_plex))
		#candidate_two_plexNew.sort()
		#print("candidate_two_plexNew "+str(candidate_two_plexNew))
		#print candidate_two_plexNew
		#print type(candidate_two_plex[0])
		#print "---------------------------------"+str(candidate_two_plexNew)
		#tmppl = [str(candidate_two_plexNew[0])]   # ATTENZIONE: NESSUNO LO USA?
		
		#print tmppl
		#checkDuplicate = complete_two(tmppl,pl,G)
		#print "Complete 1  "+str(checkDuplicate)
		
		#checkDuplicate2 = complete_tree(checkDuplicate,cliques)
		
		#print "Complete 2  "+str(checkDuplicate2)
		#print "c      "+str(c)
		#print "c      "+str(c)
		#if compare(checkDuplicate2,x[0]):
		#print "compare"

		#isMaximal = 1
				
		isMaximal = checkMaximality(candidate,dualConflictG)
		if isMaximal == 0:
			continue  # discard this 2-plex because it is not maximal

		numberOf2plex = numberOf2plex+1	
		candidate_two_plex.sort()
		output_file.write("%s\n" % str(candidate_two_plex))

	# Delete the dual of conflict-graph 
	#
	dualConflictG.clear()
	
	return numberOf2plex

##################################################################################

# Costruisce e ritorna il duale del grafo dei conflitti.
# Il grafo dei conflitti ha come nodi:
#   (a) I singoli nodi del grafo originale e 
#   (b) I non-archi del grafo originale (cioe' gli archi del duale). 
# Gli archi del grafo dei conflitti sono di tre tipi:
#   (1) Ci sono archi tra ogni coppia di nodi "nodi" che hanno tra loro un non-arco. 
#       Non vogliamo prendere entrambi gli estemi di un non-arco: in questo caso va 
#       preso il non-arco che e' piu' espressivo in termini di vincoli.
#   (2) Ci sono archi tra nodi "non-archi" e i loro estremi "nodi": se prendi un non-arco
#       hai gia' preso i suoi estremi.
#   (3) C'e' un arco tra un nodo "non-arco" e un nodo "nodo" che, se presi insieme,
#       formano una taboo triple.
#  (3') C'e' un arco tra due nodi "non-arco" che, se presi insieme, formano una taboo triple.
 
def dualConflictGraph(dual,original):

	# Inizio da un grafo vuoto
    #
	dualConflictG = nx.Graph()
	
	# Introduco i nodi di cui al punto (a).
	# Sarebbe lo stesso prendere original.nodes()
	#
	dualConflictG.add_nodes_from(dual.nodes()) 

	# Introduco i nodi di cui al punto (b).
	#
	for edge in dual.edges():
		dualConflictG.add_node(edge[0]+"-"+edge[1])

    # Inserisco gli archi del punto (1). Siccome sto costruendo il grafo duale
    # e siccome tra i nodi di tipo (a) ci sono solo gli arci del punto (1), allora
	# inserisco gli archi di G invece dei non-archi di G.
	#
	dualConflictG.add_edges_from(original.edges()) # copio gli archi tra i due grafi

	# Ora introduco gli archi di cui al punto (2) e (3).
	# Per ogni nodo del grafo dei conflitti:
	#
	for node in dualConflictG.nodes():
		# print(node) # DEBUG
		# preparo una lista di nodi del grafo che se presi insieme al nodo
		# corrente formano una taboo triple (cioe' una terna che induce un
		# cammino di lunghezza due nel duale).
		# 
		listTemp = []

		# Ricerco i due nodi nodeCurrent[0] e nodeCurrent[1]
		# che sono gli estremi del non-arco che ha dato vita al
		# nodo corrente (di tipo (b))
		#
		nodeCurrent = node.split("-")
		#print nodeCurrent
		if len(nodeCurrent) > 1:  # cioe' solo se il nodo e' di tipo (b)
			neigh0 = dual.neighbors(nodeCurrent[0])
			neigh1 = dual.neighbors(nodeCurrent[1])

			# Metto in listTemp gli adiacenti (nel grafo duale di G) degli estremi 
			# del non-arco. Se questi nodi sono presi insieme al non-arco corrente
			# formo una taboo triple perche' ho preso due non-archi consecutivi:
			# il non-edge corrente e il non-edge che porta al nodo di listTemp.
			# ATTENZIONE: un nodo potrebbe essere messo in lista due volte.
			# ATTENZIONE: questa lista contiene anche gli stessi nodeCurrent[0] e [1] che
			#             quindi figurano come incompatibili con la coppia "node" determinando
			#             l'inserimento degli archi di tipo (2).
			#
			for v in neigh0:
				listTemp.append(v)
			for v in neigh1:
				listTemp.append(v)
			
			# Per ogni altro nodo node2 del grafo dei conflitti (devo verificare
			# che non contenga elementi di listTemp).
			#
			for node2 in dualConflictG.nodes():

				if node!=node2:
					#print node2
					nodeCurrent2 = node2.split("-")

					# se anche node2 nasce da un non-arco
					#
					if len(nodeCurrent2) > 1:

						# Se uno dei due estremi di node2 e' in listTemp allora c'e' un 
                        			# conflitto tra node2 e node => l'arco (node,node2) fa parte del 
						# grafo dei conflitti (non lo devo inserire nel duale del grafo
						# dei conflitti) altrimenti, se nessuno
						# dei due estremi di node2 e' in listTemp, aggiungo l'arco (node,node2)
						# al duale del grafo dei conflitti.
						#
						if nodeCurrent2[0] not in listTemp and nodeCurrent2[1] not in listTemp:
							dualConflictG.add_edge(node,node2)
					
					# altrimenti (se node2 nasce da un nodo)
					#
					else:

						# Se il nodo node2 e' in listTemp allora c'e' un conflitto 
						# tra node e node2, altrimenti lo aggiungo al duale del 
						# grafo dei conflitti.
						#
						if nodeCurrent2[0] not in listTemp:
							dualConflictG.add_edge(node,node2)
					
	return dualConflictG

##################################################################################

# Costruisce (e ritorna) il grafo duale del grafo passato come paramentro 
# (cioe' il grafo che ha un arco per ogni non-arco di tale grafo)
#
def dual(graph):

    # Comincio da un grafo vuoto
	#
	dualG = nx.Graph()

	# Aggiungo i nodi del grafo originale
	# 
	dualG.add_nodes_from(graph.nodes())

	# Aggiungo i non-archi
	#
	for n in dualG.nodes():
		# mi procuro la lista dei non-archi di ogni nodo n
		#
		nonN = nx.non_neighbors(graph, n)

		# Aggiungo a dualG i non-archi (ATTENZIONE: un non-arco viene aggiunto due 
		# volte, una volta per ogni suo estremo. Occorre verificare che la 
		# seconda aggiunta non abbia effetto?).
        #
		for n1 in nonN:
			dualG.add_edge(n,n1)

	return dualG

##################################################################################

# Prende in input una insieme di nodi (candidates) e il grafo (graph).
# Ritorna 0 se i nodi in candidates formano una clique.
# Ritorna 1 se i nodi in candidates non formano una clique.
# Questa funzione e' usata da checkMaximality

def checkClique(candidates,graph):
	check = 0 
	for n in candidates:
		# print('***')
		# print('Nodo ' + n)
		#neighbors = graph.neighbors(n)
		listNeighbors = list(graph.neighbors(n))
		#print listNeighbors
		for n1 in candidates:
			# print('Nodo Verifica ' + n1)
			if n != n1:
				if n1 not in listNeighbors:
					# print('Nodo ' + n1 + ' non contenuto nei neighbors')
					check = 1 # non e' una clique, ritornero' 1
					break
			# 	'''else:
			# 		print 'ok'
			# else:
			# 	print 'Uguali' '''
		if check == 1:
			break			
	return check		

##################################################################################
	
# checkMaximality(twoplex,dualConflictGraph)
# Usata da due_plexes_of_component().
# Ritorna 1 se il 2-plesso passato in input e' massimale. 
# Ritorna 0 se il 2-plesso passato in input non e' massimale.
#
def checkMaximality(twoplex,dualConflictGraph):
	setNodes = set(dualConflictGraph.nodes())
	isMaximal = 1   # assumo che sia massimale
	for node in twoplex:
		if isMaximal==1:
			# print("------------------") # DEBUG
			trueNode = node.split("-")
			# print(trueNode) # DEBUG
			if len(trueNode)==1:  # se questo nodo nasce da un nodo di G
 
				# Devo provare a sostituire questo nodo con un nodo che nasce da un non-arco di G.
				# Mi servono i nodi del conflictGraph che: (1) nascono dai non-archi di G;
                # (2) contengono "node"; e (3) sono compatibili con tutti i nodi del
				# 2-plesso dato.
				# 
				neighborsNonN = list(dualConflictGraph.neighbors(node))
				neighborsN = list(setNodes-set(neighborsNonN))  # vicini di "node" nel conflictGraph
				for nei in neighborsN:
					if isMaximal == 1:
						#print nei
						trueNei = nei.split("-")
						if len(trueNei)>1:
							if str(trueNei[0])==str(node) or str(trueNei[1])==str(node):
								tmpClique = twoplex[:]
								tmpClique.remove(node)
								tmpClique.append(nei)
								#print "tmpClique"
								#print tmpClique
								check = checkClique(tmpClique,dualConflictGraph)
								#print "Check"
								#print check
								if check==0: # i nodi formano una clique dopo l'aggiunta di "nei"
									isMaximal=0 # quindi il due plesso originale non era massimale.

	return isMaximal

##################################################################################

# Attualmente nessuno usa complete
#
def complete(clique,nodes,graph):
	newclique = clique[:]
	for node in nodes:
		
		tmpclique = newclique[:]
		tmpclique.append(node)
		check = checkClique(tmpclique,graph)
		if check==0:
			newclique.append(node)
	return newclique

##################################################################################

# Attualmente nessuno usa complete_two
#
def complete_two(clique,nodes,graph):
	#print nodes
	sub = graph.subgraph(nodes)
	#print "nodi : "+str(sub.nodes())
	if len(sub.nodes())!=0:
		clisub = list(nx.find_cliques(sub))

		clisub.sort(key=len,reverse=True)
		return clisub[0]
	else:
		return []

##################################################################################

# Usato da complete_tree (che comunque non usa nessuno)
#
def intersect(a, b):
    return list(set(a) & set(b))

##################################################################################

# Attualmente nessuno usa la funzione complete_three
#
def complete_tree(clique,cliques):
	finalCLique = []
	if len(clique)!=0:
		#print "nodi : "+str(graph.nodes())
		clisub = cliques[:]
		clisub.sort(key=len,reverse=True)
		for c in clisub:
			newCliqu = intersect(c,clique)
			if compare(newCliqu,clique):
				finalCLique = c
				break
		if len(finalCLique)==0:
			finalCLique = clique
	return finalCLique

##################################################################################

# Prende una lista di triple e la trasforma in 
# una lista di coppie, omettendo l'elemento centrale.
# Attualmente non la chiama nessuno.
#	
def convert(lista):
	newList = []
	for val in lista:
		tmp = (val[0],val[2])
		newList.append(tmp) 
	return newList

##################################################################################

# Attualmente non la chiama nessuno
#
def neighborsList(nodes,graph):
	neighborsList=[]
	neighborsListCorrect = []
	for node in nodes:
		neighborsList.append(node)
		neighbors = list(graph.neighbors(node))
		for el in neighbors:
			neighborsList.append(el)
	
	neighborsListCorrect = set(list(neighborsList))
	return sorted(neighborsListCorrect)

##############################################################
############ FINE DELLE DEFINIZIONI DELLE FUNZIONI ###########
##############################################################

########## INIZIO PROGRAMMA ###########

# if args.verbose: print("%s: Leggo il file %s contenente il grafo" % (sys.argv[0],args.file))


# commentato da titto per farlo girare in locale
#
# sc = SparkContext()
# inFile = sc.textFile(sys.argv[1])

#inFile = sc.textFile("hdfs:///user/user16/input/"+sys.argv[1])

#G = nx.read_edgelist("hdfs:///user/user16/input/ca-GrQc.nde-nodistr")

start_ts = time.time()
st = datetime.datetime.fromtimestamp(start_ts).strftime('%Y-%m-%d %H:%M:%S.%f')
#print(st)
# print("\n--- INIZIO COMPUTAZIONE (" + st + ") -------")

# rdd is a Spark resilient distributed database

#rdd = inFile.map(lambda x : x.split("$")).mapValues(lambda y :y.split(","))\
#		.map(lambda x : ("1",two_plex(x)))

#lineList = inFile.readlines()
x = []
x.append([])  # sarebbe la lista dei nodi ma non mi serve, quindi ce ne metto una vuota
#x.append([line.rstrip('\n') for line in open(sys.argv[1])])
x.append([line.rstrip('\n') for line in open(args.file)])
# print(x[0]) # DEBUG
# print(x[1]) # DEBUG
# la stampa di x[1] e' del tipo ['1 2', '1 3', '1 5', '2 3', '2 4', '2 5', '3 4', '4 5', '4 6', '5 6']

output_file= open(args.output,"w+")
# if args.verbose: print("%s: Output nel file %s" % (sys.argv[0],args.output))

if args.algo == "basic":
	risultato = two_plexes_basic(x)
elif args.algo == "comp_by_comp":
	risultato = two_plexes_comp_by_comp(x)

output_file.close()


end_ts = time.time()
st = datetime.datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d %H:%M:%S.%f')
#rdd.saveAsTextFile("hdfs:///user/user16/output/"+sys.argv[1]+"/"+st+"/")
#print(st)
# print("----- FINE COMPUTAZIONE (" + st + ") -------\n")

if args.algo == "basic":
	print("   CIKM-B: seconds for enumerating %d %s 2-plexes: %f" % (risultato,args.type,(end_ts - start_ts)) )
elif args.algo == "comp_by_comp":
	print("CIKM-CbyC: seconds for enumerating %d %s 2-plexes: %f" % (risultato,args.type,(end_ts - start_ts)) )

#'''
#.flatMapValues(lambda x : x)\
#.map(lambda x : (str(x[1]),x[0]))\
#.map(lambda x: x[0])
#'''




