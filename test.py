import networkx as nx

from aminer.readers import CoAuthorReader, AuthorReader

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

