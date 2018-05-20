#!/usr/bin/python
import os, sys
import graph_gen

def ballots_to_bump_edge_count(nodes, source, target):
    others = filter(lambda node: node != source and node != target, nodes)
    if len(others) == 0:
        ballot = [[source], [target]]
        return [ballot]
    ballot1 = [[source], [target], others]
    ballot2 = [others, [source, target]]
    return [ballot1, ballot2]

def ballot_to_line(ballot):
    parts = map(lambda candidates: '='.join(candidates), ballot)
    return '>'.join(parts)

def ballots_to_text(ballots=[]):
    return '\n'.join(map(ballot_to_line, ballots))

def main():
    if len(sys.argv) != 4:
        print 'Usage: graph-gen.py <number of graphs> <max node count> <out dir>'
        return
    graph_count = int(sys.argv[1])
    max_node_count = int(sys.argv[2])
    out_dir = sys.argv[3]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for graph_num,graph in enumerate(graph_gen.gen_graphs(graph_count, 2, max_node_count)):
        print graph
        nodes = graph['nodes']
        edges = graph['edges']
        ballots = []
        for edge in graph['edges']:
            ballots.extend(ballots_to_bump_edge_count(nodes, edge['source'], edge['target']))
        ballots_text = ballots_to_text(ballots)
        print ballots_text
        out_path = os.path.join(out_dir, '%d.txt'%graph_num)
        with open(out_path, 'w') as f:
            f.write(ballots_text + '\n')

if __name__ == '__main__':
    main()
