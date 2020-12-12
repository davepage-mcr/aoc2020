#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of instructions")
parser.add_argument("--debug",    action='store_true')
args = parser.parse_args()

class Point:
    def __init__ (self, x = 0, y = 0):
        self.x = x
        self.y = y

class AbsPoint(Point):
    def movetowards( self, way, times ):
        if args.debug:
            print("\tMoving towards", ( way.x, way.y ), times)
        self.x += way.x * times
        self.y += way.y * times

    def manhattan( self ):
        return abs(self.x) + abs(self.y)

class RelPoint(Point):
    def move( self, action, num ):
        if args.debug:
            print("\tMoving", num, action)
    
        if action == 'N':
            self.y += num
        elif action == 'S':
            self.y -= num
        elif action == 'E':
            self.x += num
        elif action == 'W':
            self.x -= num
   
    def rotate (self, action, num ):
        if action == 'L':
            num = -num
        if num % 90 != 0:
            raise ValueError ("Non right angle turn of {}".format(num))
        turns = int( num / 90 ) % 4
        if args.debug:
            print("\tPerforming", turns, "right-hand turns")
        for i in range(turns):
            # ( x, y ) rotated around (0,0) goes to ( y, -x )
            newx = self.y
            newy = -self.x

            self.x = newx
            self.y = newy
    
hovercraft = AbsPoint(0,0)
waypoint = RelPoint(10,1)

inputfile = open( args.inputfile )
for line in inputfile:
    action = line[0]
    num=int(line[1:])

    if args.debug:
        print("Instruction:", action, num)

    if action == 'N' or action == 'S' or action == 'E' or action == 'W':
        waypoint.move(action, num)
    elif action == 'L' or action == 'R':
        waypoint.rotate(action, num)
    elif action == 'F':
        hovercraft.movetowards(waypoint, num)
    else:
        raise ValueError("Unrecognised action {}".format(action))

    if args.debug:
        print("\tHovercraft is at", (hovercraft.x, hovercraft.y), "Waypoint is", (waypoint.x, waypoint.y))

print( hovercraft.manhattan() )
