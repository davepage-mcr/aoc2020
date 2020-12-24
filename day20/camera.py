#!/usr/bin/env python3

import sys
import argparse
from itertools import combinations

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of camera data")
parser.add_argument("--debug",    action='store_true', help="Debug")
args = parser.parse_args()

class Tile:
    def __init__(self, tileid, tiledata):
        self.id = tileid
        self.tiledata = []

        left = ''
        right = ''

        for line in tiledata:
            left += line[0]
            self.tiledata.append( line[1:-1] )
            right += line[-1]

        # A tile has 4 edges, can rotate 4 ways, can match on 4 sides (top,
        # right, bottom, left)

        # +---+ +---+
        # | a | | p |
        # |b c| |q r|
        # | d | | s |
        # +---+ +---+

        # If both these tiles can rotate freely, sometimes we're matching
        # reverses against forwards. Can probably optimise this but just do all
        # edges forwards and backwards for now

        self.edges = [ tiledata[0], right, tiledata[-1], left ]

    def __repr__(self):
        return "Tile #{}".format( self.id )

tiles = set()

with open( args.inputfile ) as inputfile:
    tiledata = []
    for line in inputfile:
        line = line.strip()
        if line[0:4] == 'Tile':
            tileid = int(line[5:-1])
        elif line == '':
            tiles.add( Tile(tileid, tiledata ) )
            tiledata = []
        else:
            tiledata.append(line)
    tiles.add( Tile(tileid, tiledata ) )

print("We have {} tiles".format(len(tiles)))

# Now consider all pairs of tiles and see which edges match

matches = {}

for x, y in combinations(tiles, 2):
    print("Checking matches for {} and {}".format(x, y))
    for xedge in x.edges:
        for yedge in y.edges:
            if xedge == yedge:
                print("\t{} matches {}".format(xedge, yedge))
            elif xedge == yedge[::-1]:
                print("\t{} matches reversed {}".format(xedge, yedge))
            else:
                continue
            if x.id not in matches:
                matches[x.id] = set()
            if y.id not in matches:
                matches[y.id] = set()
            matches[x.id].add( y.id )
            matches[y.id].add( x.id )

# We know the corner tiles are the ones which match exactly 2 other tiles, and
# there are four corners.

for tile in matches:
    print( tile, matches[tile], len(matches[tile]) )

corners = [ x for x in matches if len(matches[x]) == 2 ]
if len(corners) != 4:
    print("We don't have four corners, something is messed up")
    exit(1)

product = 1
for corner in corners:
    product *= corner

print("Product of corners is {}".format(product))
