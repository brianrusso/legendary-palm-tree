import networkx as nx

class AMinerGraph(object):
    G = None

    def __init__(self, authors, coauthor_relations):
        self.G = nx.Graph()
        self.add_authors(authors)
        self.add_coauthor_relations(coauthor_relations)


    def add_authors(self, authors):
        for key in authors:
            self.G.add_node(key, authors[key])


    def add_coauthor_relations(self, coauthor_relations):
        for author in coauthor_relations.keys():  # for each author
            for rel in coauthor_relations[author]:  # each author can have multiple relations
                # don't think i have to do this...
                #author_a_node = self.G[author]
                #author_a_node = self.G[rel[0]]
                self.G.add_edge(author, rel[0], weight=rel[1])