#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of initial cube state")
parser.add_argument("--debug",    action='store_true', help="Debug")
parser.add_argument("--flat",    action='store_true', help="Ignore Z plane")
args = parser.parse_args()

cubes = None

neighbours = set()
for z in [0] if args.flat else range(-1, 2):
    for y in range(-1, 2):
        for x in range(-1, 2):
            if z == 0 and y == 0 and x == 0:
                continue
            neighbours.add( tuple([ x, y, z ]) )
if args.debug:
    print("We have {} possible neighbours for each cube".format( len(neighbours) ))

class Constellation:
    def __init__(self, minx, maxx, miny, maxy, minz, maxz):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

        if args.flat:
            self.minz = 0
            self.maxz = 0
        else:
            self.minz = minz
            self.maxz = maxz

        self.pos = {}
        for z in [0] if args.flat else range(minz, maxz+1):
            self.pos[z] = {}
            for y in range(miny, maxy+1):
                self.pos[z][y] = {}
                for x in range(minx, maxx+1):
                    self.pos[z][y][x] = False
        self.numactive = 0

    def set(self, x, y, z, active):
        former = self.get(x,y,z)
        self.pos[z][y][x] = active
        if former == False and active == True:
            self.numactive += 1
        elif former == True and active == False:
            self.numactive -= 1

    def get(self, x, y, z):
        if z not in self.pos:
            return False
        if y not in self.pos[z]:
            return False
        if x not in self.pos[z][y]:
            return False
        return self.pos[z][y][x]

    def print(self, cycle):
        print("### State at cycle", cycle)
        for z in range(self.minz, self.maxz + 1):
            print("# z = {}".format(z))
            for y in range(self.miny, self.maxy + 1):
                print("y = {:3}  ".format(y), end='')
                for x in range(self.minx, self.maxx + 1):
                    print("#" if self.pos[z][y][x] == True else '.', end='')
                print()
        print("{} active cubes".format( self.numactive ))

    def evolve(self):
        newcon = Constellation(self.minx-1, self.maxx+1,
                                self.miny-1, self.maxy+1,
                                self.minz-1, self.maxz+1)

        for z in [0] if args.flat else range(self.minz-1, self.maxz+2):
            for y in range(self.miny-1, self.maxy+2):
                for x in range(self.minx-1, self.maxx+2):
                    if args.debug:
                        print("Looking to set coords {} in next gen".format( (x,y,z) ))
                    oldstate = self.get( x,y,z )
                    newstate = None
                    activeneighbours = 0
                    for pn in neighbours:
                        # print("\tLooking at {} relative to {}: {} is {}".format( pn, (x,y,z), ( x+pn[0], y+pn[1], z+pn[2] ), self.get(x+pn[0], y+pn[1], z+pn[2] )))
                        if self.get(x+pn[0], y+pn[1], z+pn[2] ) == True:
                            activeneighbours += 1
                    if args.debug:
                        print("Coords {} was {}; has {} active neighbours".format( (x,y,z), oldstate, activeneighbours))
                    if oldstate == True:
                        if activeneighbours == 2 or activeneighbours == 3:
                            newstate = True
                        else:
                            newstate = False
                    else:
                        if activeneighbours == 3:
                            newstate = True
                        else:
                            newstate = False

                    newcon.set( x,y,z, newstate )

        return(newcon)

cycle = 0
with open( args.inputfile ) as inputfile:
    y=0
    for line in inputfile:
        if cubes == None:
            width = len( line.strip() )
            if args.debug:
                print("Creating new constellation {}x{}x1".format(width,width))
            cubes = Constellation(0, width-1, 0, width-1, 0, 0)

        for x in range(len(line.strip())):
            cubes.set(x, y, 0, line[x] == '#')

        y += 1

cubes.print(cycle)

for cycle in range(1,7):
    cubes = cubes.evolve()
    cubes.print(cycle)
    cycle += 1

