#!/usr/bin/python
import graph_gen
from collections import defaultdict as ddict

def get_winner(graph):
    win_count = ddict(int)
    nodes = graph['nodes']
    for node in nodes:
        won = True
        for edge in graph['edges']:
            if edge['source'] == node:
                win_count[node] += 1
                if win_count[node] == len(nodes) - 1:
                    return node # this one has an edge pointing to everybody else
    return None

def drop_nodes(graph, drop):
    nodes = filter(lambda node: node not in drop , graph['nodes'])
    edges = filter(lambda edge: edge['source'] not in drop and edge['target'] not in drop, graph['edges'])
    return {'nodes': nodes, 'edges': edges}

def get_condorcet_rankings(graph):
    cur = graph
    order = []
    rank = 1
    while True:
        winner = get_winner(cur)
        if winner == None:
            return order
        order.append({'rank': rank, 'candidate': winner})
        cur = drop_nodes(cur, [winner])
        rank += 1

def main():
    graph = graph_gen.random_gen_size(node_count=4)
    print graph
    print get_condorcet_rankings(graph)

if __name__ == '__main__':
    main()
