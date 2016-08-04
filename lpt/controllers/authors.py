from flask import Blueprint, render_template, flash, request, redirect, url_for
from lpt.extensions import cache
from lpt.models import db
from json import loads, dumps
import networkx as nx
from networkx.readwrite import json_graph


authors = Blueprint('authors', __name__)

def get_authorcoll():
    coll = db.collection("authors")
    return coll

@authors.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')



@authors.route('/authors')
@cache.cached(timeout=1000)
def list_authors():
    return dumps(get_authorcoll().first(5))


@authors.route('/v1/authors/<key>.json')
@cache.cached(timeout=10000)
def get_author(key):
    return dumps(get_authorcoll().document(key))

@authors.route('/v1/authors_by_tech/<term>.json')
@cache.cached(timeout=10000)
def get_authors_from_tech(term):
    cursor = db.execute_query(
        "FOR d in authors FILTER @val IN d.terms[*] RETURN d",
        bind_vars={"val": term}
    )
    authors = []
    for doc in cursor:
        authors.append(doc)
    return dumps(authors)

@authors.route('/v1/authors_by_name/<name>.json')
@cache.cached(timeout=10000)
def get_authors_from_name(name):
    cursor = db.execute_query(
        "FOR d in FULLTEXT(authors, \"name\", @val) RETURN d",
        bind_vars={"val": name}
    )
    authors = []
    for doc in cursor:
        authors.append(doc)
    return dumps(authors)

#@authors.route('/authors/<key>/neighbors.json')
#@cache.cached(timeout=10000)
#def get_author_neighbors(key):
#    return dumps(_get_author_neighbors(key))


@authors.route('/v1/authors/<key>/<distance>-neighbors.json')
@cache.cached(timeout=10000)
def get_author_neighbors(key, distance):
    return dumps(list(_get_variable_neighborhood(key, int(distance))))

@authors.route('/v1/authors/<key>/<distance>-graph.json')
@cache.cached(timeout=10000)
def get_author_neighbors_nx(key, distance):
    return dumps(json_graph.node_link_data(_get_variable_neighborhood_as_nx(key, int(distance))))


# HTML

@authors.route('/authors/<key>/<distance>-graph.html')
@cache.cached(timeout=10000)
def get_author_neighbors_nx_force(key, distance):
    return render_template('authors/node_forcegraph.html', key=key, distance=int(distance))



def _get_author_neighbors(key):
    key = "authors/" + key
    cursor = db.execute_query(
        "FOR V IN 1..1 ANY @val GRAPH \"aminer_coauthors\" RETURN V._key",
        bind_vars={"val": key}
    )
    authors = []
    for doc in cursor:
        authors.append(doc)
    return authors

def _get_variable_neighborhood(key, distance):
    if distance <= 0:
        raise Exception("Distance must be >= 1")
    elif distance == 1:
        return set(_get_author_neighbors(key))
    else:
        results = set(_get_author_neighbors(key))
        for neighbor in _get_author_neighbors(key):
            new_set = _get_variable_neighborhood(neighbor, distance-1)
            results = results.union(new_set)
        return results

def _get_variable_neighborhood_as_nx(key, distance):
    g = nx.Graph()
    if distance <= 0:
        raise Exception("Distance must be >= 1")
    elif distance == 1:
        results = set(_get_author_neighbors(key))
        for neighbor in results:
            g.add_node(neighbor)
            g.add_edge(neighbor, key)
        return g
    else:
        results = set(_get_author_neighbors(key))
        # prime with immediate neighbors
        for neighbor in results:
            g.add_node(neighbor)
            g.add_edge(neighbor, key)
        # recurse to neighbors
        for neighbor in results:
            new_set = _get_variable_neighborhood(neighbor, distance-1)
            for their_neighbor in new_set:
                g.add_node(their_neighbor)
                g.add_edge(their_neighbor, neighbor)
            results = results.union(new_set)
        return g
