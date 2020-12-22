#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of initial cube state")
parser.add_argument("--debug",    action='store_true', help="Debug")
args = parser.parse_args()

cubes = None

hyperneighbours = set()
for w in range(-1, 2):
    for z in range(-1, 2):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if z == 0 and y == 0 and x == 0 and w == 0:
                    continue
                hyperneighbours.add( tuple([ x, y, z, w ]) )
if args.debug:
    print("We have {} possible neighbours for each cube".format( len(hyperneighbours) ))

class HyperConstellation:
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, minw, maxw):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

        self.minz = minz
        self.maxz = maxz
        self.minw = minw
        self.maxw = maxw

        self.pos = {}
        for w in range(minw, maxw+1):
            self.pos[w] = {}
            for z in range(minz, maxz+1):
                self.pos[w][z] = {}
                for y in range(miny, maxy+1):
                    self.pos[w][z][y] = {}
                    for x in range(minx, maxx+1):
                        self.pos[w][z][y][x] = False
        self.numactive = 0

    def set(self, x, y, z, w, active):
        former = self.get(x,y,z, w)
        self.pos[w][z][y][x] = active
        if former == False and active == True:
            self.numactive += 1
        elif former == True and active == False:
            self.numactive -= 1

    def get(self, x, y, z, w):
        if w not in self.pos:
            return False
        if z not in self.pos[w]:
            return False
        if y not in self.pos[w][z]:
            return False
        if x not in self.pos[w][z][y]:
            return False
        return self.pos[w][z][y][x]

    def print(self, cycle):
        print("### State at cycle", cycle)
        for w in range(self.minw, self.maxw + 1):
            for z in range(self.minz, self.maxz + 1):
                print("# z = {}, w = {}".format(z, w))
                for y in range(self.miny, self.maxy + 1):
                    print("y = {:3}  ".format(y), end='')
                    for x in range(self.minx, self.maxx + 1):
                        print("#" if self.pos[w][z][y][x] == True else '.', end='')
                    print()
        print("{} active cubes".format( self.numactive ))

    def evolve(self):
        newcon = HyperConstellation(self.minx-1, self.maxx+1,
                                self.miny-1, self.maxy+1,
                                self.minz-1, self.maxz+1,
                                self.minw-1, self.maxw+1)

        for w in range(self.minw-1, self.maxw+2):
            for z in range(self.minz-1, self.maxz+2):
                for y in range(self.miny-1, self.maxy+2):
                    for x in range(self.minx-1, self.maxx+2):
                        if args.debug:
                            print("Looking to set coords {} in next gen".format( (x,y,z,w) ))
                        oldstate = self.get( x,y,z,w )
                        newstate = None
                        activeneighbours = 0
                        for pn in hyperneighbours:
                            if self.get(x+pn[0], y+pn[1], z+pn[2], w+pn[3]) == True:
                                activeneighbours += 1
                        if args.debug:
                            print("Coords {} was {}; has {} active neighbours".format(
                                (x,y,z,w), oldstate, activeneighbours))
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

                        newcon.set( x,y,z,w, newstate )

        return(newcon)

cycle = 0
with open( args.inputfile ) as inputfile:
    y=0
    for line in inputfile:
        if cubes == None:
            width = len( line.strip() )
            if args.debug:
                print("Creating new hyperconstellation {}x{}x1x1".format(width,width))
            cubes = HyperConstellation(0, width-1, 0, width-1, 0, 0, 0, 0)

        for x in range(len(line.strip())):
            cubes.set(x, y, 0, 0, line[x] == '#')

        y += 1

cubes.print(cycle)

for cycle in range(1,7):
    cubes = cubes.evolve()
    cubes.print(cycle)
    cycle += 1

