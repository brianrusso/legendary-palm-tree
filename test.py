import networkx as nx

from aminer.readers import CoAuthorReader, AuthorReader
from aminer.graph import make_aminer_graph
from aminer.util import nodes_by_affil
import json
from networkx.readwrite import json_graph

# FIXME: hard-coded
AUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Author.txt"
COAUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Coauthor.txt"
AUTHOR2PAPER_FILE = "/brokenwillow/AMiner/AMiner-Author2Paper.txt"
PAPER_FILE = "/brokenwillow/AMiner/AMiner-Paper.txt"

g = nx.Graph()

author_reader = AuthorReader(AUTHOR_FILE)
coauthor_reader = CoAuthorReader(COAUTHOR_FILE)

# dict with author_idx as key, contains Author objects
authors = author_reader.get_records()

# dict with author_a_idx as key (matches authors)
# contains list of tuples [(author_b_idx, num_articles), ...]
coauthor_relations = coauthor_reader.get_records()

G = make_aminer_graph(authors, coauthor_relations)


#H = nx.Graph(G.edges([807866]))
H = nx.Graph([(u,v,d) for u,v,d in G.edges(data=True) if d['weight'] > 30])
subgraph_json = json_graph.node_link_data(H)
out = open('30_graph.json','w')
json.dump(subgraph_json, out)

# Highly connected SAR dude - Mehrdad Soumekh (Iranian EE - NB: No reason to believe he's bad, just an example)
# len(G.nodes())
# 1712433
# Who he's connected to?
# mehrdad = nx.shortest_path(G, 1679207).keys()
# len(mehrdad)
# 1057194 .. wow!


# Find all nodes that mention Wright Patterson
#wp = nodes_by_affil(G, "Wright Patterson")
#wp = wp + nodes_by_affil(G, "WrightPatterson")
#len(wp) => 503
# Find all nodes that mention China
# china_nodes = nodes_by_affil(G, "China")
# Get all their neighbors
#china_neighbors1 = neighborhood_of_list(G, china_nodes, 1)
# Intersection of China + Wright Patt mentions
#china_neighbors_1.intersection(wp)
#len(china_neighbors_1) =>197342
#{115124, 165609, 209039, 267800, 548278, 715779, 780207, 800548, 835823, 1151035, 1372721, 1655824, 1673968}
# These guys..
# Guna Seetharaman (1673968)
#Richard K. Martin (715779)
#Yongcan Cao (800548)
#John L. Fleming (165609)
#Kyle A. Novak (209039)
#Eswar Josyula (1655824)
#Jonathan T. Goldstein (1372721)
#Daniel W. Repperger (115124)
#A H Klopf (548278)
#X.-G. Xia (267800)
#Matthew Fickus (1151035)
#Aihua W. Wood (780207)
#Miguel R. Visbal (835823)
# Let's look at Yongcan Cao.. interested in AUVs, cyber, sensors, etc..
# degrees from Nanjing University of Aeronautics & Astronautics & Shanghai Jiao Tong University

# stuff for bfs
#foo = nx.subgraph(G, nx.algorithms.bfs_successors(G, 0))  # 0 is root
