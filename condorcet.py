#!/usr/bin/python
import graph_gen

def get_winners(graph):
    winners = set()
    for node in graph['nodes']:
        won = True
        for edge in graph['edges']:
            if edge['target'] == node:
                won = False
                break
        if won:
            winners.add(node)
    return winners

def drop_nodes(graph, drop):
    nodes = filter(lambda node: node not in drop , graph['nodes'])
    edges = filter(lambda edge: edge['source'] not in drop and edge['target'] not in drop, graph['edges'])
    return {'nodes': nodes, 'edges': edges}

def get_condorcet_rankings(graph):
    cur = graph
    results = []
    rank = 1
    while True:
        winners = get_winners(cur)
        if len(winners) == 0:
            return results
        results.append({'rank': rank, 'candidates': list(winners)})
        cur = drop_nodes(cur, winners)
        rank += 1

def main():
    graph = graph_gen.random_gen_size(node_count=4)
    print graph
    print get_condorcet_rankings(graph)

if __name__ == '__main__':
    main()
