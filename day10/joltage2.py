#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of adapters")
parser.add_argument("--debug",  action='store_true', help="Print debug")
args = parser.parse_args()

# Slurp integers from file into set
adapters = []
inputfile = open( args.inputfile )
for line in inputfile:
    adapters.append( int(line) )
adapters = sorted(adapters)
paths = [0]

# First find the joltage of our device
target = max(adapters) + 3
print("Our target joltage is", target)

def buildpath( start, gen, startpos ):
    if start + 3 == target:
        paths[0] += 1
        return

    # Check the next 3 adapters to see if we can connect to them
    for i in range( startpos, startpos + 3):
        if i >= len(adapters):
            break
        if adapters[i] <= start + 3:
            buildpath( adapters[i], gen+1, i+1 )
    return

buildpath(0, 0, 0)

print(paths[0])
