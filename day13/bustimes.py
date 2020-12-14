#!/usr/bin/env python3

import sys
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of instructions")
parser.add_argument("--time",     type=int, help="Start part 2 at this time", default=1)
parser.add_argument("--debug",    action='store_true')
args = parser.parse_args()

with open( args.inputfile ) as inputfile:
    departure = int(inputfile.readline())
    allbuses = inputfile.readline().strip().split(',')
    buses = [ int(i) for i in allbuses if i != 'x' ]

firstline = None
firsttime = None

for bus in buses:
    depart = bus * math.ceil( departure / bus )

    if firsttime is None or depart < firsttime:
        firsttime = depart
        firstline = bus

print("First bus to depart after", departure, "is", firstline, "at", firsttime)
print("Part 1", firstline * ( firsttime - departure ))

# Now part 2
t = args.time
valid = False
while valid == False:
    t += 1
    valid = True

    if args.debug:
        print("### Time", t)

    for i in range(len(allbuses)):
        if allbuses[i] == 'x':
            continue
        mintodepart = ( t + i ) % int(allbuses[i])

        if args.debug:
            print("Bus {:3} must depart {} minutes after {}, at {}; departs {} minutes after that".format(
            allbuses[i], i, t, t + i, mintodepart))

        if mintodepart != 0:
            valid = False
            break

print("Bus departures sync up at", t)
