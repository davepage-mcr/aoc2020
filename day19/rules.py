#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of sums")
parser.add_argument("--debug",    action='store_true', help="Debug")
args = parser.parse_args()

rules = {}
matches = 0

# Definitions:
# depth: how far down we are - just used for debugging really
# remnant: the text left over after matching a rule
# tofollow: ther ules that remain (which may expand to sub-rules)

def validatebynum( text, rulenum, depth, tofollow ):
    rule = rules[rulenum]
    return( validate( text, rule, rulenum, depth, tofollow ) )

def validate( text, rule, ruleid, depth, tofollow ):
    if len(text) == 0:
        return ( False, None )

    if args.debug:
        print("{} Rule {}: We need to validate {} against '{}' followed by {}".format(
            '~' * depth, ruleid, text, rule, tofollow))

    if rule[0] == '"':
        # Text rule; if the start of text matches, return the remnant, else False
        matchme = rule[1:-1]
        if text[:len(matchme)] == matchme:
            print("{} Rule {}: Text '{}' matches rule '{}' with remnant '{}'".format('*' * depth, ruleid, text, matchme, text[len(matchme):] ))
            return( True, text[len(matchme):] )
        else:
            print("{} Rule {}: Text {} fails match {}".format('*' * depth, ruleid, text, matchme))
            return( False, None ) 
    elif '|' in rule:
        # Optional rules; must split on | and check each one
        subrules = rule.split(' | ')
        print("{} Rule {}: Text {} must match any of {}".format( '-' * depth, ruleid, text, subrules ))
        for srn in range(len(subrules)):
            # ( matched, remnant ) = validate(text, subrules[srn], '{}.{}'.format(ruleid, srn), depth + 1)
            pass

    else:
        # This should be a list of numbers of sub-rules to follow
        subrules = [ int(x) for x in rule.split() ]
        print("{} Rule {}: must match all of {}".format( '-' * depth, ruleid, subrules ))
        for i in range(len(subrules)):
            srnum = subrules[i]
            subtofollow = subrules[i+1:]
            ( matched, text ) = validatebynum(text, srnum, depth + 1, subtofollow)
            if matched == False:
                return(False, None)
        print("{} Rule {}: we have matched all rules, '{}' remains".format( '-' * depth, ruleid, text ))
        return(True, text)

with open( args.inputfile ) as inputfile:
    for line in inputfile:
        if line.strip() == '':
            continue
        elif line[0] == '#':
            continue
        elif ':' in line:
            ( num, rule ) = line.strip().split(': ')
            rules[int(num)] = rule
        else:
            # This is something to match against our rules
            print("### Validating", line.strip())
            ( matched, remnant ) = validatebynum(line.strip(), 0, 0, [])
            if matched == True and remnant == '':
                print("Line {} completely matches rule 0".format(line.strip()))
                matches += 1

print("We have {} matches".format(matches))
