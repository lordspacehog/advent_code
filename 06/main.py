#!/usr/bin/env python3
import argparse
import networkx as nx


def main():
    G = nx.DiGraph()

    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    args = parser.parse_args()

    with open(args.inputfile, 'r') as filep:
        G.add_edges_from(
            map(
                lambda x: x.split(')'),
                filep.read().rstrip().split('\n')
            )
        )

    root = list(nx.topological_sort(G))[0]
    csum = sum(map(lambda x: len(x)-1,
                   nx.single_source_bellman_ford_path(G, root).values()))

    print(f'checksum: {csum}')

    san_parent = list(G.predecessors('SAN'))[0]
    you_parent = list(G.predecessors('YOU'))[0]
    shortest_path = nx.shortest_path_length(G.to_undirected(),
                                            source=you_parent,
                                            target=san_parent)
    print(f'shortest path to san is: {shortest_path}')


if __name__ == '__main__':
    main()
