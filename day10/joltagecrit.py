#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of adapters")
parser.add_argument("--debug",  action='store_true', help="Print debug")
parser.add_argument("--dot",  action='store_true', help="Print a graphviz dot graph")
parser.add_argument("--up",  action='store_true', help="Try to work up from target")
args = parser.parse_args()

# Slurp integers from file into set
adapters = set()
inputfile = open( args.inputfile )
for line in inputfile:
    adapters.add( int(line) )
foundpaths = 0

# First find the joltage of our device
target = max(adapters) + 3
if args.debug:
    print("Our target joltage is", target)

adapters.add(0)
adapters.add(target)

# Now build a tree of which adapters can connect to which adapters
children = {}
parents = {}
for a in adapters:
    for i in range(1,4):
        if a+i in adapters:
            if a not in children:
                children[a] = set()
            children[a].add(a+i)
            if a+i not in parents:
                parents[a+i] = set()
            parents[a+i].add(a)

# Find any childless nodes (except target)

if args.dot:
    print("digraph children {")

for node in children:
    if args.dot:
        print(node, "-> {", ', '.join(str(x) for x in children[node]), "}")
    else:
        if len(children[node]) == 0:
            print(node, "is childless; room for optimisation")
        elif len(children[node]) == 1:
            print(node, "is on a critical path")

if args.dot:
    print("}")
    exit()

def buildpathup( node ):
    global foundpaths

    if node == 0:
        foundpaths += 1
        return

    for c in parents[node]:
        buildpathup( c )
