#!/usr/bin/python
import os, sys, json, argparse
import graph_gen, condorcet, visualize

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
    parser = argparse.ArgumentParser(description='Generate some graphs and ballots')
    parser.add_argument('-c', '--count', metavar='c', type=int, default=1,
                        help='number of graphs')
    parser.add_argument('-n', '--nodes', metavar='n', type=int, default=4,
                        help='number of nodes')
    parser.add_argument('-w', '--winners', metavar='w', type=int, default=0,
                        help='number of extra winners in addition to "n" nodes')
    parser.add_argument('-o', '--out_dir', metavar='o', type=str, default='out',
                        help='directory in which to dump output')
    args = parser.parse_args()
    
    graph_count = args.count
    max_node_count = args.nodes
    extra_winners = args.winners
    out_dir = args.out_dir

    if os.path.exists(out_dir):
        print 'Dir %s already exists' % out_dir
        sys.exit(1)
    os.mkdir(out_dir)

    for graph_num,graph in enumerate(graph_gen.gen_graphs(graph_count, 2, max_node_count)):
        for i in range(extra_winners):
            name = 'W%d' % (extra_winners - i)
            graph_gen.add_winner(graph, name)
        
        print graph
        nodes = graph['nodes']
        edges = graph['edges']

        # gen ballots
        all_tie_ballot = [[n for n in nodes]]
        ballots = [all_tie_ballot]
        for edge in graph['edges']:
            ballots.extend(ballots_to_bump_edge_count(nodes, edge['source'], edge['target']))
        ballots_text = ballots_to_text(ballots)
        print ballots_text
        out_path = os.path.join(out_dir, '%d.txt'%graph_num)
        with open(out_path, 'w') as f:
            f.write(ballots_text + '\n')

        # gen condorcet results
        results = condorcet.get_condorcet_rankings(graph)
        out_path = os.path.join(out_dir, '%d-results.json'%graph_num)
        with open(out_path, 'w') as f:
            f.write(json.dumps(results) + '\n')

        # visualize graph
        graph_dir = os.path.join(out_dir, '%d-graph'%graph_num)
        visualize.generate_alchemy_graph(graph, graph_dir)

if __name__ == '__main__':
    main()
