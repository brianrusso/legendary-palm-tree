import networkx as nx
from aminer.readers import AuthorReader, CoAuthorReader

from arango import Arango


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

def get_author_coauthors(author_file, coauthor_file):
    author_reader = AuthorReader(author_file)
    coauthor_reader = CoAuthorReader(coauthor_file)
    authors = author_reader.get_records()
    coauthor_relations = coauthor_reader.get_records()
    return (authors, coauthor_relations)


def setup_graph(author_file, coauthor_file):
    authors, coauthor_relations = get_author_coauthors(author_file, coauthor_file)
    g = make_aminer_graph(authors, coauthor_relations)
    return g

# python-arango version
def load_into_arango(author_file, coauthor_file):
    authors, coauthor_relations = get_author_coauthors(author_file, coauthor_file)

    a = Arango(host="localhost", port=8529)
    try:
        db = a.create_database("aminer")
    except:
        db = a.database("aminer")

    try:
        graph = db.create_graph("aminer_coauthors")
    except:
        graph = db.graph("aminer_coauthors")

    try:
        db.create_collection("authors")
        graph.create_vertex_collection("authors")
        db.create_collection("coauthors", is_edge=True)
        graph.create_edge_definition(edge_collection="coauthors",
                                from_vertex_collections=["authors"],
                                 to_vertex_collections=["authors"])
    except:
        pass

    for key in authors:
        graph.create_vertex("authors", authors[key])
    for author in coauthor_relations.keys():
        for rel in coauthor_relations[author]:
            graph.create_edge("coauthors", {"_from": "authors/" + unicode(author),
                                            "_to": "authors/"+ unicode(rel[0]),
                                            "w": rel[1]})

