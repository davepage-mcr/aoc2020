#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of adapters")
parser.add_argument("--debug",  action='store_true', help="Print debug")
parser.add_argument("--dot",  action='store_true', help="Print a graphviz dot graph")
args = parser.parse_args()

# Slurp integers from file into set
adapters = set()
inputfile = open( args.inputfile )
for line in inputfile:
    adapters.add( int(line) )
# First find the joltage of our device
target = max(adapters) + 3
if args.debug:
    print("Our target joltage is", target)

adapters.add(0)
adapters.add(target)

# Now build a tree of which adapters can connect to which adapters
children = {}
critical = []
for a in adapters:
    for i in range(1,4):
        if a+i in adapters:
            if a not in children:
                children[a] = set()
            children[a].add(a+i)
            if i == 3 and len(children[a]) == 1:
                critical.append(a)

# Find any childless nodes (except target)
if args.dot:
    print("digraph children {")

for node in sorted(children):
    if args.dot:
        print(node, "-> {", ', '.join(str(x) for x in children[node]), "}")
    else:
        if len(children[node]) == 0:
            print(node, "is childless; room for optimisation")

if args.dot:
    print("}")
    exit()

def buildpathdown( node, target ):
    if node == target:
        return 1

    paths = 0
    for c in children[node]:
        paths += buildpathdown( c, target )
    return paths

# To get anywhere in this space, we have to go through *all* the nodes in critical[]
# Work out all the ways to get between critical nodes, then multiply them together
# By definition there is only one way from the last adapter to the target device
totways = 1
for i in range(0, len(critical)):
    if i == 0:
        start = 0
    else:
        start=critical[i-1]
    dest = critical[i]

    ways = buildpathdown(start, dest)
    if args.debug:
        print("There are", ways, "ways are there to get from", start, "to", dest)
    totways *= ways

print(totways)
