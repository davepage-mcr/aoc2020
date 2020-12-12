#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of instructions")
parser.add_argument("--debug",    action='store_true')
args = parser.parse_args()

class Craft:
    def __init__ (self):
        self.dir = 'E'
        self.x = 0
        self.y = 0

    def handle(self, action, num):
        if args.debug:
            print("Interpreting", action, num, "; currently", (self.x, self.y), self.dir)
        if action == 'N':
            self.y += num
        elif action == 'S':
            self.y -= num
        elif action == 'E':
            self.x += num
        elif action == 'W':
            self.x -= num
        elif action == 'F':
            self.handle(self.dir, num)
        elif action == 'R':
            if num % 90 != 0:
                raise ValueError("Non-right angle turn", num)
            turns = int( num / 90 )
            if args.debug:
                print("\tExecuting", turns , "right turns")
            dirs = [ 'N', 'E', 'S', 'W' ]
            for i in range(len(dirs)):
                if dirs[i] == self.dir:
                    self.dir = dirs[(i+turns) % 4]
                    break
        elif action == 'L':
            self.handle('R', -num)
        else:
            raise ValueError("Unrecognised action", action)

        if args.debug:
            print("\tNow", (self.x, self.y), self.dir)

    def distance (self):
        return abs(self.x) + abs(self.y)

hovercraft = Craft()

inputfile = open( args.inputfile )
for line in inputfile:
    action = line[0]
    num=int(line[1:])

    hovercraft.handle(action, num)

print( hovercraft.distance() )
