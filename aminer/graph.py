import networkx as nx
from readers import AuthorReader, CoAuthorReader


def make_aminer_graph(authors, coauthor_relations):
    g = nx.Graph()
    g = add_authors(g, authors)
    g = add_coauthor_relations(g, coauthor_relations)
    return g

def add_authors(graph, authors):
    for key in authors:
        graph.add_node(key, authors[key])
    return graph


def add_coauthor_relations(graph, coauthor_relations):
    for author in coauthor_relations.keys():  # for each author
        for rel in coauthor_relations[author]:  # each author can have multiple relations
            # don't think i have to do this...
            #author_a_node = self.G[author]
            #author_a_node = self.G[rel[0]]
            graph.add_edge(author, rel[0], weight=rel[1])
    return graph


def setup_graph(author_file, coauthor_file):
    author_reader = AuthorReader(author_file)
    coauthor_reader = CoAuthorReader(coauthor_file)
    authors = author_reader.get_records()
    coauthor_relations = coauthor_reader.get_records()
    g = make_aminer_graph(authors, coauthor_relations)
    return g
