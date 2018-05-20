#!/usr/bin/python
import random, sys

FORWARD = 'forward'
BACKWARD = 'backward'
NEITHER = 'neither'
SOURCE = 'source'
TARGET = 'target'

def random_gen_size(node_count=1):
    nodes = map(str, range(node_count))
    edges = []
    for nodeA in range(len(nodes)):
        for nodeB in range(nodeA+1, len(nodes)):
            edge_type = random.choice([FORWARD, BACKWARD, NEITHER])
            if edge_type == FORWARD:
                edges.append({SOURCE: nodes[nodeA], TARGET: nodes[nodeB]})
            elif edge_type == BACKWARD:
                edges.append({SOURCE: nodes[nodeB], TARGET: nodes[nodeA]})
    return {'nodes': nodes, 'edges': edges}

def gen_graphs(graph_count, min_node_count, max_node_count):
    graphs = []
    for i in range(graph_count):
        node_count = random.randint(min_node_count,max_node_count)
        yield random_gen_size(node_count)

def main():
    if len(sys.argv) != 3:
        print 'Usage: graph-gen.py <number of graphs> <max node count>'
        return
    graph_count = int(sys.argv[1])
    max_node_count = int(sys.argv[2])
    for graph in gen_graphs(graph_count, 2, max_node_count):
        print '='*40
        print graph

if __name__ == '__main__':
    main()
