
def nodes_by_attr(graph, attr_name, attr_val):

    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if d[attr_name] == attr_val:
            nodes.append(p)
    return nodes


def nodes_by_affil(graph, term):
    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if term in d['affil']:
            nodes.append(p)
    return nodes


def nodes_by_term(graph, term):

    nodes = list()
    for (p, d) in graph.nodes(data=True):
        if term in d['terms']:
            nodes.append(p)
    return nodes


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

# Be careful with distance ! Can get really big
def neighborhood_of_list(graph, nodes, distance):
    results = set()
    for node in nodes:
        results = results.union(neighborhood(graph, node, distance))
    return results