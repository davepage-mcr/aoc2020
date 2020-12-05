#!/usr/bin/python3

import sys
from itertools import combinations
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of seats")
args = parser.parse_args()

maxseatid = 0
seatids = set()

# Slurp integers from file into array
with open( args.inputfile ) as inputfile:
    for line in inputfile:
        minrow = 0
        maxrow = 127
        mincol = 0
        maxcol = 7
        for inst in line.strip():
            if inst == 'F':
                # Front of current range, reduce maxrow
                maxrow = minrow + int(( maxrow - minrow ) / 2)
            elif inst == 'B':
                # Back of current range, increase minrow
                minrow = minrow + int(( maxrow - minrow ) / 2 + 0.5)
            elif inst == 'L':
                # Left side; decrease maxcol
                maxcol = mincol + int(( maxcol - mincol ) / 2)
            elif inst == 'R':
                # Right side, increase mincol
                mincol = mincol + int(( maxcol - mincol ) / 2 + 0.5)
            else:
                print("Unexpected instruction", inst)
                break

        if minrow != maxrow:
            print("End of instructions, still have a range of", minrow, maxrow)
            continue

        if mincol != maxcol:
            print("End of instructions, still have a range of", mincol, maxcol)
            continue

        seatid = minrow * 8 + mincol
        seatids.add(seatid)
        if seatid > maxseatid:
            maxseatid = seatid

        print("Seat is at", minrow, mincol, "id", seatid)

print("Max seat ID", maxseatid)

for i in range(0,maxseatid):
    # i isn't in set, i-1 and i+1 are
    if ( not i in seatids ) and (i-1) in seatids and (i+1) in seatids:
        print("Our seat could be", i)
