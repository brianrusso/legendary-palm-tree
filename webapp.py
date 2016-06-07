from flask import Flask, render_template

import networkx as nx
import json
import pickle
from aminer.util import get_attached_subgraph, graph_to_d3tree_json, \
    graph_to_d3nodelink_json, mst_from_graph, bfs_from_tree, neighborhood, \
    deep_subgraph

app = Flask(__name__)

# FIXME: this is a hack for demo purposes
# TODO - Move data into graph database
app.G = pickle.load(open('littleG.pickle'))


@app.route('/')
def index():
    return "Hello!"

@app.route('/authors/')
def get_authors():
    return render_template('nodes.html', nodes=app.G.nodes())


@app.route('/authors/<idx>.nodejson')
def get_neighbors_nodejson(idx):
    subgraph = get_attached_subgraph(app.G, int(idx))
    return graph_to_d3nodelink_json(subgraph)

@app.route('/authors/<idx>.treejson')
def get_neighbors_treejson(idx):
    #subgraph = get_attached_subgraph(app.G, int(idx))
    subgraph = deep_subgraph(app.G, neighborhood(app.G, int(idx), 2))
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
    #try:
    record = app.G.node[int(idx)]
    return render_template('node.html', node=record, neighbors=app.G[int(idx)].keys())
    #except:
    #    return str(idx) + " not found"

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8000)