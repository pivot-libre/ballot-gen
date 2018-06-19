#!/usr/bin/python
import random, sys
from collections import defaultdict as ddict
import graph_gen, visualize

def parse(text):
    nodes = set()
    edge_counts = ddict(int) # key: (src,dst), val: count
    
    for line in text.split('\n'):
        if line.strip() == '':
            continue
        ballot = [part.split('=') for part in line.split('>')]
        for i, group1 in enumerate(ballot):
            for group2 in ballot[i+1:]:
                for A in group1:
                    nodes.add(A)
                    for B in group2:
                        edge_counts[(A,B)] += 1 # A beats B in this ballot

    nodes = list(nodes)
    edges = []
    for i,A in enumerate(nodes):
        for B in nodes:
            margin = edge_counts[(A,B)] - edge_counts[(B,A)]
            if margin > 0:
                edges.append({graph_gen.SOURCE: A, graph_gen.TARGET: B, 'label': str(margin)})
            elif margin < 0:
                edges.append({graph_gen.SOURCE: B, graph_gen.TARGET: A, 'label': str(-margin)})

    return {'nodes': nodes, 'edges': edges}

def main():
    if len(sys.argv) != 3:
        print 'Usage: graph_parse.py <path> <out-dir>'
        return
    path,outdir = sys.argv[1:]
    with open(path) as f:
        text = f.read()
    graph = parse(text)
    visualize.generate_alchemy_graph(graph, outdir)

if __name__ == '__main__':
    main()
