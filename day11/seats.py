#!/usr/bin/env python3

import sys
import argparse
import copy

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file map of lounge")
parser.add_argument("--debug",  action='store_true', help="Print debug")
parser.add_argument("--part2",  action='store_true', help="Part 2: visibility not adjacent")
args = parser.parse_args()

# We want lounge to be a 2D array of chars

lounge = []
inputfile = open( args.inputfile )
for line in inputfile:
    lounge.append( list(line.strip()) )

def adjacent(row, col, lplan):
    neighbours = 0

    for nc, nr in [ (col-1,row-1), (col, row-1), (col+1, row-1),
                  (col-1,row),                 (col+1, row),
                  (col-1,row+1), (col, row+1), (col+1, row+1) ]:
        if nc < 0 or nr < 0 or nr >= len(lplan) or nc >= len(lplan[0]):
            # Skip this
            continue
        if lplan[nr][nc] == '#':
            neighbours += 1

    if( args.debug ):
        print("Seat at", ( col, row), "has", neighbours )
    return(neighbours)

def visible (row, col, lplan ):
    neighbours = 0

    # Look for first seat in 8 cardinal directions from (col, row)
    for dc, dr in [ (-1, -1),  ( 0, -1 ),  ( 1, -1 ),
                    (-1,  0),              ( 1,  0 ),
                    (-1, +1),  ( 0,  1 ),  ( 1,  1 ) ]:

        occupied = False

        r = row + dr
        c = col + dc

        while r >= 0 and r < len( lplan ) and c >= 0 and c < len( lplan[0] ):
            if lplan[r][c] == '#':
                occupied = True
                break
            elif lplan[r][c] == 'L':
                break

            r += dr
            c += dc

        if occupied:
            neighbours += 1

    return(neighbours)

def evolve(oldplan):
    plan = copy.deepcopy(oldplan)
    maxoccupied = 4
    if args.part2:
        maxoccupied = 5


    for row in range(len(plan)):
        for col in range(len(plan[0])):
            if plan[row][col] == '.':
                continue
            else:
                if args.part2:
                    occupied = visible ( row, col, oldplan )
                else:
                    occupied = adjacent( row, col, oldplan )
                if oldplan[row][col] == 'L' and occupied == 0:
                    if ( args.debug ):
                        print("Seat at", (col, row), 'now occupied')
                    plan[row][col] = '#'
                elif oldplan[row][col] == '#' and occupied >= maxoccupied:
                    if ( args.debug ):
                        print("Seat at", (col, row), 'now vacated')
                    plan[row][col] = 'L'

    return(plan)

rounds = 0
while True:

    print("\n===Round", rounds)
    for line in lounge:
        print( ''.join(line) )

    newlounge = evolve(lounge)

    if newlounge == lounge:
        lounge = newlounge
        print("We have stabilised after", rounds)
        break

    rounds += 1
    lounge = newlounge

# Now count the seats in lounge
occupied = 0
for row in range(len(lounge)):
    for col in range(len(lounge[0])):
        if lounge[row][col] == '#':
            occupied += 1

print(occupied)
