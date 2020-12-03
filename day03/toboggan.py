#!/usr/bin/python3

import sys
from itertools import combinations
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of integers")
parser.add_argument("toboggans",  metavar='M', nargs='*', default=['3,1'],
                     help="Toboggan movements across,down")
parser.add_argument('--part2', action='store_true', help='Shortcut for 1,1 3,1 5,1 7,1 1,2')
args = parser.parse_args()

if args.part2:
  toboggans=['1,1', '3,1', '5,1', '7,1', '1,2']
else:
  toboggans=args.toboggans

# Slurp integers from file into array
trees = []
inputfile = open( args.inputfile )
for line in inputfile:
  trees.append(line.strip())

product = 1

# Iterate over our toboggans
for toboggan in toboggans:
  move = toboggan.split(',')
  dx = int(move[0])
  dy = int(move[1])

  posx = 0
  posy = 0
  collisions = 0

  while True:
    if trees[posy][posx] == '#':
      collisions += 1
  
    posx += dx
    posx %= len(trees[0]) # Wrap around
    posy += dy
  
    if posy >= len(trees):
      break
  
  print('{} collisions'.format(collisions))
  product *= collisions

print('Product of collisions is {}'.format(product))
