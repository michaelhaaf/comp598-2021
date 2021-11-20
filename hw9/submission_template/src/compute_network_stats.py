#!/usr/bin/env python3

import networkx as nx
import numpy as np
import json
import argparse

TOP_N = 3


def prune_connections(connections):
    return {k:v for k,v in connections.items() if v > 0}

def build_graph(network):
    g = nx.Graph()
    for node1 in network.keys():
        for node2, count in network[node1].items(): 
            g.add_edge(node1, node2, weight=count)
    return g

def most_connected_by_num(g):
    node_degrees = {v: g.degree(v) for v in g.nodes()}
    return sorted(node_degrees, key=node_degrees.get, reverse=True)[0:TOP_N]

def most_connected_by_weight(g):
    node_weights = {v: sum([e["weight"] for n, e in g[v].items()]) for v in g.nodes()}
    return sorted(node_weights, key=node_weights.get, reverse=True)[0:TOP_N]

def most_connected_by_betweenness(g):
    node_btwnness = {v: g.betweenness(v) for v in g.nodes()}
    return sorted(node_btwnness, key=node_btwnness.get, reverse=True)[0:TOP_N]


def main(args):
    in_file = open(args.inputFile, "r") 
    network = json.load(in_file)
    in_file.close() 

    network = {k: prune_connections(v) for k, v in network.items()}
    g = build_graph(network)

    stats = {
        "most_connected_by_num": most_connected_by_num(g),
        "most_connected_by_weight": most_connected_by_weight(g)
        "most_central_by_betweenness": most_connected_by_betweenness(g)
    }

    out_file = open(args.outputFile, "w") 
    json.dump(stats, out_file, indent=4)
    out_file.close() 


# USAGE:
# python compute_network_stats.py -i <interaction_network.json> -o <stats.json>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NLP network stats analysis script')
    parser.add_argument('-o', 
                        dest='outputFile',
                        required=True,
                        help='output file name. Should be a .json file',
                        type=str
                        )
    parser.add_argument('-i',
                        dest='inputFile',
                        required=True,
                        help='network file name. Should be a .json file',
                        type=str
                        )
    args = parser.parse_args()
    main(args)

