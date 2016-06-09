from flask import Flask, render_template
from flask import request
import networkx as nx
import json
import pickle
from aminer.graph import setup_graph
from aminer.util import get_attached_subgraph, graph_to_d3tree_json, \
    graph_to_d3nodelink_json, mst_from_graph, bfs_from_tree, neighborhood, \
    deep_subgraph, build_tech_index, nodes_by_affil


app = Flask(__name__)


# FIXME: this is a hack for demo purposes
# TODO - Move data into graph database
AUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Author.txt"
COAUTHOR_FILE = "/brokenwillow/AMiner/AMiner-Coauthor.txt"

#app.G = setup_graph(AUTHOR_FILE, COAUTHOR_FILE)
app.G = pickle.load(open('aminer.pickle'))
app.tech_index = build_tech_index(app.G)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tech/')
def get_techs():
    return render_template('tech_list.html', tech=app.tech_index)


@app.route('/tech/<tech_guid>')
def get_tech(tech_guid):
    tech = app.tech_index[tech_guid]
    (name, nodes) = tech
    return render_template('tech_detail.html', tech_name=name, nodes=nodes)

@app.route('/search/tech/<term>')
def search_tech(term):
    terms = list()
    for k,v in app.tech_index.iteritems():
        if term in v[0]:
            terms.append((k,app.tech_index[k]))
    return render_template('tech_list.html', tech=terms)
    #return str(terms)

@app.route('/search/affil/<term>')
def search_affil(term):
    nodes = nodes_by_affil(app.G, term)
    #return str(nodes)
    return render_template('search/affil_results.html', nodes=nodes, affil_term=term )


@app.route('/authors/')
def get_authors():
    return render_template('author_list.html', nodes=app.G.nodes())


@app.route('/authors/<idx>.nodejson')
def get_neighbors_nodejson(idx):
    subgraph = get_attached_subgraph(app.G, int(idx))
    return graph_to_d3nodelink_json(subgraph)


@app.route('/authors/<idx>.treejson')
def get_neighbors_treejson(idx):
    #subgraph = get_attached_subgraph(app.G, int(idx))
    subgraph = deep_subgraph(app.G, neighborhood(app.G, int(idx), 3))
    # Convert to tree
    tree = nx.bfs_tree(subgraph, int(idx))
    # populate attributes
    for index in tree.nodes():
        tree.node[index] = app.G.node[index]
    return graph_to_d3tree_json(tree, int(idx))


@app.route('/authors/<idx>.d3force')
def get_neighbors_d3force(idx):
    return render_template('node_forcegraph.html', idx=int(idx))


@app.route('/authors/<idx>.d3tree')
def get_neighbors_d3tree(idx):
    return render_template('node_radialtree.html', idx=int(idx))


@app.route('/authors/<idx>')
def get_author(idx):
    record = app.G.node[int(idx)]
    return render_template('author_detail.html', node=record, neighbors=app.G[int(idx)].keys())


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8000)