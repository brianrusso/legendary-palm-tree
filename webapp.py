from flask import Flask, render_template
from networkx.readwrite import json_graph
import networkx as nx
import json
import pickle

app = Flask(__name__)

app.G = pickle.load(open('littleG.pickle'))


@app.route('/')
def index():
    return "Hello!"

@app.route('/authors/')
def get_authors():
    return render_template('nodes.html', nodes=app.G.nodes())

@app.route('/authors/<idx>.json')
def get_neighbors_json(idx):
    _subgraph = nx.Graph(nx.subgraph(app.G, app.G[int(idx)]))
    d3js = json_graph.node_link_data(_subgraph)
    return json.dumps(d3js)
    #record = app.G.node[int(idx)]

@app.route('/authors/<idx>.d3')
def get_neighbors_d3(idx):
    return render_template('node_graph.html', idx=int(idx))


@app.route('/authors/<idx>')
def get_author(idx):
    #try:
    record = app.G.node[int(idx)]
    return render_template('node.html', node=record, neighbors=app.G[int(idx)].keys())
    #except:
    #    return str(idx) + " not found"

if __name__ == '__main__':
    app.debug=True
    app.run(host='192.168.1.200', port=8000)