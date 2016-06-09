import networkx as nx
import json, uuid, operator
from networkx.readwrite import json_graph
from collections import defaultdict, OrderedDict
from aminer.model import Tech


def nodes_by_attr(graph, attr_name, attr_val):
    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if d[attr_name] == attr_val:
            nodes.append(p)
    return nodes

def nodes_by_affil(graph, term):
    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if term in unicode(d['affil'],'utf-8'):
            nodes.append(p)
    return nodes


def nodes_by_term(graph, term):
    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if term in d['terms']:
            nodes.append(p)
    return nodes

def get_attached_subgraph(graph, idx):
    nodes = graph[int(idx)]  # include ourself
    nodes[int(idx)] = graph.node[int(idx)]
    _subgraph = nx.Graph(nx.subgraph(graph, nodes))
    return _subgraph


def deep_subgraph(graph, nodes):
    _subgraph = nx.Graph(nx.subgraph(graph, nodes))
    return _subgraph


def bfs_from_tree(graph, root):
    return nx.bfs_tree(graph, root)

def mst_from_graph(graph):
    return nx.minimum_spanning_tree(graph)


# Convert graph to node-link format as json string
def graph_to_d3nodelink_json(graph):
    d3js = json_graph.node_link_data(graph)
    return json.dumps(d3js)


# Convert graph to tree format as json string
def graph_to_d3tree_json(graph, root):
    d3js = json_graph.tree_data(graph, root)
    return json.dumps(d3js)


# Convert graph to tree format as json string
def graph_to_d3adjacency_json(graph):
    d3js = json_graph.adjacency_data(graph)
    return json.dumps(d3js)


# local traversal to find set of nodes within distance (1 = adjacent)
def neighborhood(graph, node_id, distance):
    if distance <= 0:
        raise Exception("Distance must be >= 1")
    elif distance == 1:
        return set(graph[node_id].keys())
    else:
        results = set(graph[node_id].keys())
        for neighbor in graph[node_id].keys():
            new_set = neighborhood(graph, neighbor, distance-1)
            results = results.union(new_set)
        return results

# Dict of tech labels, values are tuple of label + set of nodes
# we use uuids because strings are lame
def build_tech_index(graph):
    labels = defaultdict(list)
    # for each node in graph
    for n, d in graph.nodes_iter(data=True):
        # for each tech term in this node
        for tech_term in d['terms']:
            # place the node id in the dict with tech as key
            # lower case
            tech_term = str(tech_term.lower())
            guid = uuid.uuid3(uuid.NAMESPACE_URL, tech_term).hex
            # add this node to its tech term
            try:
                labels[guid][1].update({n})
            except:
                labels[guid] = (tech_term, {n})
    return labels
    #return OrderedDict(sorted(labels.items(), key=operator.itemgetter(0)))


# Be careful with distance ! Can get really big
def neighborhood_of_list(graph, nodes, distance):
    results = set()
    for node in nodes:
        results = results.union(neighborhood(graph, node, distance))
    return results

