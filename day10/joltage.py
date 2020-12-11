#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of adapters")
parser.add_argument("--debug",  action='store_true', help="Print debug")
parser.add_argument("--part2",  action='store_true', help="Part 2: Consider all arrangements")
args = parser.parse_args()

# Slurp integers from file into set
inputfile = open( args.inputfile )
adapters = set()
for line in inputfile:
    adapters.add( int(line) )

# First find the joltage of our device
target = max(adapters) + 3
print("Our target joltage is", target)
adapters.add(target)

def adapt( source, ltarget, chain, steps ):
    if source == ltarget:
        print("We have reached", ltarget, "via", chain)
        if len(chain) == len(adapters):
            print("This uses all adapters")
            return steps

    if args.debug:
        print("What can we connect to a source of", source, "at the end of", chain)
    for s in range(1, 4):
        j = source + s
        if j in adapters:
            if args.debug:
                print("We have an adapter rated", j, "; step up of", s)
            lchain = chain
            lchain.append(j)
            steps[s] += 1
            if not args.part2:
                return adapt(j, ltarget, lchain, steps)

            adapt(j, ltarget, lchain, steps)

steps = {}
for i in range(1,4):
    steps[i] = 0

finsteps = adapt(0, target, [], steps )
print( steps[1] * steps[3] )
