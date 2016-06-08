import uuid


class Tech(object):
    nodes = {}

    def __init__(self, name):
        self.name = name


class Author(object):

    def __init__(self, author_idx, name, affiliation, pc, cc, hindex, pindex, upindex, terms):
        self.author_idx = author_idx
        self.name = name
        self.affiliation = affiliation
        self.pc = pc  # published count (number of articles)
        self.cc = cc  # citation count
        self.hindex = hindex
        self.pindex = pindex
        self.upindex = upindex
        self.terms = terms  # list of topics

    def as_dict(self):
        output = dict()
        output['_type'] = "A"
        output['idx'] = self.author_idx
        output['name'] = self.name
        output['affil'] = self.affiliation
        output['pc'] = self.pc
        output['cc'] = self.cc
        # not using this right now
        #output['hidx'] = self.hindex
        #output['pidx'] = self.pindex
        #output['upidx'] = self.upindex
        output['terms'] = self.terms
        return output



class Paper(object):

    def __init__(self, paper_idx, title, authors, affiliation, year, venue, refs, abstract):
        self.paper_idx = paper_idx
        self.title = title
        self.authors = authors
        self.affiliation = affiliation
        self.year = int(year) if year else None
        self.venue = venue
        self.refs = refs
        self.abstract = abstract if abstract else None