#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of adapters")
parser.add_argument("--debug",  action='store_true', help="Print debug")
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
for node in children:
    if node != target and len(children[node]) == 0:
        print(node, "is childless; room for optimisation")

# Find any orphan nodes (except 0)
for node in parents:
    if node != 0 and len(parents[node]) == 0:
        print(node, "is orphaned; room for optimisation")

def buildpathdown( node ):
    global foundpaths

    if node == target:
        foundpaths += 1
        return

    for c in children[node]:
        buildpathdown( c )

def buildpathup( node ):
    global foundpaths

    if node == 0:
        foundpaths += 1
        return

    for c in parents[node]:
        buildpathup( c )

if args.up:
    if args.debug:
        print("Parents:", parents)
    buildpathup(target)
else:
    if args.debug:
        print("Children:", children)
    buildpathdown(0)

print(foundpaths)
