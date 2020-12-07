#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of rules")
args = parser.parse_args()

rule = re.compile('^(.*) bags contain (.*).$')
contentre = re.compile('^(\d+|no) (.*) bags?$')

ruledown = {}
ruleup = {}

targetcolour = 'shiny gold'

# Parse our rules
inputfile = open( args.inputfile )
for line in inputfile:
    match = rule.match(line)
    if match == None:
        print("Failed to match", line.strip())
        continue
    rulefor = match.group(1)
    if rulefor not in ruledown:
        ruledown[rulefor] = []

    for contents in match.group(2).split(', '):
        cont = contentre.match(contents)
        if cont == None:
            print("Failed to match", contents)
            continue
        if cont.group(1) == 'no':
            continue
        contnum = int(cont.group(1))
        contcol = cont.group(2)

        ruledown[rulefor].append( tuple(( int(cont.group(1)), cont.group(2) )) )
        if contcol not in ruleup:
            ruleup[contcol] = []
        ruleup[contcol].append(rulefor)

def whatcontains( target ):
    if target not in ruleup or len(ruleup[target]) == 0:
        # Nothing contains this; return
        return set()

    total = set()
    for container in ruleup[target]:
        total.add(container)
        total |= whatcontains(container)
    return(total)


print(len(whatcontains(targetcolour)), "colours can contain", targetcolour)

def howmanyin(target):
    if len(ruledown[target]) == 0:
        return 0

    total = 0
    for contents in ruledown[target]:
        total += contents[0]
        total += contents[0] * howmanyin(contents[1])

    return total

print(howmanyin(targetcolour), 'bags inside one', targetcolour)
