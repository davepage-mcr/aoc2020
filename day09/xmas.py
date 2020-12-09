#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of numbers")
parser.add_argument("--preamble",  type=int, help="Specify preamble length", default=25)
args = parser.parse_args()

def is_summable( target, candidates ):
    for prospect in candidates:
        if 2*prospect != target and ( target-prospect ) in candidates:
            return True

    return False

preamble = args.preamble

# Slurp integers from file into array
inputfile = open( args.inputfile )
numbers = []
for line in inputfile:
    numbers.append( int(line) )

# Now find the number that isn't the sum of two of the previous $preamble numbers
invalid_at = None
for i in range(preamble, len(numbers)):
    candidates = set( numbers[i-preamble:i] )
    if not is_summable(numbers[i], candidates):
        print("Cannot sum", numbers[i], "from", candidates)
        invalid_at = i
        break

# Check we actually had an invalid number
if invalid_at == None:
    print("We didn't find an invalid number in part 1")
    exit(1)

target = numbers[invalid_at]

# Now we're basically playing blackjack
for i in range(invalid_at):
    # Sum numbers from position i upwards until they equal or top target
    total = 0
    for j in range(i, invalid_at):
        total += numbers[j]
        if total >= target:
            break

    if total == target:
        contrange = numbers[i:j+1]
        print(contrange, "sum to", target)
        print("Weakness is", min(contrange) + max(contrange))
        break
