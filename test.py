import networkx as nx

from aminer.readers import CoAuthorReader, AuthorReader
from aminer.graph import AMinerGraph
import json
from networkx.readwrite import json_graph

# FIXME: hard-coded
AUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Author.txt"
AUTHOR2PAPER_FILE = "/brokenwillow/AMiner/AMiner-Author2Paper.txt"
COAUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Coauthor.txt"
PAPER_FILE = "/brokenwillow/AMiner/AMiner-Paper.txt"

g = nx.Graph()

author_reader = AuthorReader(AUTHOR_FILE)
coauthor_reader = CoAuthorReader(COAUTHOR_FILE)

# dict with author_idx as key, contains Author objects
authors = author_reader.get_records()

# dict with author_a_idx as key (matches authors)
# contains list of tuples [(author_b_idx, num_articles), ...]
coauthor_relations = coauthor_reader.get_records()

G = AMinerGraph(authors, coauthor_relations)


#H = nx.Graph(G.edges([807866]))
H = nx.Graph([(u,v,d) for u,v,d in G.edges(data=True) if d['weight'] > 30])
subgraph_json = json_graph.node_link_data(H)
out = open('30_graph.json','w')
json.dump(subgraph_json, out)

