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

def indent( gen ):
    return("{:2d} {}".format(gen, '#' * gen))

def buildpath( dest, adapused, adapleft ):
    gen = len(adapused)
    start = adapused[-1]
    if args.debug:
        print(indent(gen), "Building from", start, adapused, "to", dest, "using", adapleft)

    if start + 3 == dest:
        if args.debug:
            print(indent(gen), "Complete path", adapused) 
        paths[0] += 1
        return

    # Check the next 3 adapters in adapleft to see if we can connect to them
    for i in range( min(3, len(adapleft) ) ):
        if adapleft[i] <= start + 3:
            if args.debug:
                print(indent(gen), "We can connect from", start, "to", adapleft[i])
            nadapused = adapused.copy()
            nadapused.append( adapleft[i] )

            nadapleft = adapleft.copy()
            buildpath( dest, nadapused, nadapleft[i+1:] )
    return

buildpath(target, [0], adapters)

print(paths[0])
