
import re, csv
from collections import defaultdict
from model import Author, Paper


class CoAuthorReader(object):

    filename = None

    def __init__(self, filename):
        self.filename = filename

    def get_records(self):
        links = defaultdict(list)
        # format is '#<authora_idx>\t<authorb_idx>\t<collabs>' per line
        with open(self.filename,'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            for line in tsv:
                author_a = line[0][1:]  # trim leading '#'
                author_b = line[1]
                collabs = line[2]
                links[int(author_a)].append((int(author_b), int(collabs)))
        return links


class AuthorReader(object):
    id_pattern = re.compile("#index([^\r\n]*)")
    name_pattern = re.compile("#n([^\r\n]*)")
    affiliation_pattern = re.compile("#a([^\r\n]*)")
    published_count_pattern = re.compile("#pc ([0-9]*)")
    citations_pattern = re.compile("#cn ([0-9]*)")
    hindex_pattern = re.compile("#hi([^\r\n]*)")
    pindex_pattern = re.compile("#pi([^\r\n]*)")
    upindex_pattern = re.compile("#upi([^\r\n]*)")
    terms_pattern = re.compile("#t([^\r\n]*)")

    fd = None

    def __init__(self, filename):
        self.fd = open(filename, 'r')

    def get_record(self):
        try:
            author_idx = int(self.id_pattern.findall(self.fd.readline())[0].strip())
        except IndexError:
            raise EOFError
        author_name = self.name_pattern.findall(self.fd.readline())[0].strip()
        affiliation = self.affiliation_pattern.findall(self.fd.readline())[0].strip()
        line = self.fd.readline()
        # it matches the PC pattern..
        if self.published_count_pattern.match(line):
            # stuff it into PC
            published_count = self.published_count_pattern.findall(line)[0].strip()
        else:  # probably an errant continuation of affiliation
            affiliation = affiliation + line  # so concatenate it to existing affiliation line
            # and then read in the next line as published_count
            published_count = self.published_count_pattern.findall(self.fd.readline())[0].strip()
        citation_count = self.citations_pattern.findall(self.fd.readline())[0].strip()
        hindex = self.hindex_pattern.findall(self.fd.readline())[0].strip()
        pindex = self.pindex_pattern.findall(self.fd.readline())[0].strip()
        upindex = self.upindex_pattern.findall(self.fd.readline())[0].strip()
        terms = self.terms_pattern.findall(self.fd.readline())[0].strip()
        line = self.fd.readline()
        # there's an error in like 8181450 where a term list spans 2 lines
        if line.strip():
            terms = terms + line
            self.fd.readline()  # skip next line
        else:
            pass  # already skipped

        terms = [a for a in terms.split(';') if a]

        return Author(
            author_idx=author_idx,
            name=author_name,
            affiliation=affiliation,
            pc=published_count,
            cc=citation_count,
            hindex=hindex,
            pindex=pindex,
            upindex=upindex,
            terms=terms
        )

    def get_records(self):
        authors = dict()
        try:
            while True:  # bad style? meh...
                author = self.get_record()
                authors[author.author_idx] = author.as_dict()
        except EOFError:
            pass
        return authors


class PaperReader(object):
    id_pattern = re.compile("#index([^\r\n]*)")
    title_pattern = re.compile("#\*([^\r\n]*)")
    author_pattern = re.compile("#@([^\r\n]*)")
    affiliations_pattern = re.compile("#o([^\r\n]*)")
    year_pattern = re.compile("#t ([0-9]*)")
    venue_pattern = re.compile("#c([^\r\n]*)")
    refs_pattern = re.compile("#%([^\r\n]*)")
    abstract_pattern = re.compile("#!([^\r\n]*)")

    fd = None

    def __init__(self, filename):
        self.fd = open(filename, 'r')

    def get_record(self):
        try:
            paper_id = int(self.id_pattern.findall(self.fd.readline())[0].strip())
        except IndexError:
            raise EOFError
        paper_title = self.title_pattern.findall(self.fd.readline())[0].strip()
        paper_authors = self.author_pattern.findall(self.fd.readline())[0].strip()
        paper_authors = [a for a in paper_authors.split(',') if a]
        paper_affiliations = self.affiliations_pattern.findall(self.fd.readline())[0].strip()
        if paper_affiliations == '-':
            paper_affiliations = None
        paper_year = self.year_pattern.findall(self.fd.readline())[0].strip()
        paper_venue = self.venue_pattern.findall(self.fd.readline())[0].strip()
        paper_refs = list()
        paper_abstract = None

        # references
        line = self.fd.readline()
        m = self.refs_pattern.match(line)
        while m is not None:
            if m:
                paper_refs.append(int(self.refs_pattern.findall(line)[0].strip()))
            line = self.fd.readline()
            m = self.refs_pattern.match(line)
        if len(paper_refs) == 0:
            paper_refs = None
        if line.strip():
            try:
                paper_abstract = self.abstract_pattern.findall(line)[0].strip()
            except:
                paper_abstract = None

        # skip if blank + consume
        #if not line.strip(): fd.readline()

        return Paper(
            paper_idx=paper_id,
            title=paper_title,
            authors=paper_authors,
            affiliation=paper_affiliations,
            year=paper_year,
            venue=paper_venue,
            refs=paper_refs,
            abstract=paper_abstract
        )

    def get_records(self):
        papers = dict()
        try:
            while True: # bad style? meh...
                paper = self.get_record()
                papers[paper.paper_idx] = paper
        except EOFError:
            pass
        return papers
