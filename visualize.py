#!/usr/bin/python
import os, sys, json, shutil
import graph_gen

CODE_DIR = os.path.dirname(__file__)

def generate_alchemy_graph(graph, outdir):
    # convert to alchemy format
    alchemy = {'nodes': [], 'edges': []}
    for node in graph['nodes']:
        caption = node
        alchemy['nodes'].append({'id': node, 'caption': caption})
    for edge in graph['edges']:
        e = {'source': edge[graph_gen.SOURCE], 'target': edge[graph_gen.TARGET]}
        # TODO: figure out whether Alchemy supports edge labels
        if 'label' in edge:
            e['label'] = edge['label']
        alchemy['edges'].append(e)
    js = json.dumps(alchemy)

    if os.path.exists(outdir):
        print 'Directory %s already exists' % outdir
        return

    os.makedirs(outdir)
    src = os.path.join(CODE_DIR, 'alchemy')
    dst = os.path.join(outdir, 'alchemy')
    shutil.copytree(src, dst)
    with open(os.path.join(CODE_DIR, 'alchemy-template.htm')) as f:
        html = f.read()
    html = html.replace('<GRAPH_DATA>', js)
    with open(os.path.join(outdir, 'graph.htm'), 'w') as f:
        f.write(html)

    print 'generated in %s' % os.path.join(outdir, 'graph.htm')

def main():
    outdir = sys.argv[1]
    graph = {'nodes': ['0','1','2'],
             'edges': [{'source': '0', 'target': '1'},
                       {'source': '1', 'target': '2'},
                       {'source': '2', 'target': '0'}]}
    generate_alchemy_graph(graph, outdir)

if __name__ == '__main__':
    main()
