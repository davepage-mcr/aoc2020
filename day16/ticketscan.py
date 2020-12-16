#!/usr/bin/env python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of ticket rules")
parser.add_argument("--debug",    action='store_true', help="Part 1 debug")
parser.add_argument("--debug2",    action='store_true', help="Part 2 debug")
args = parser.parse_args()

rules = set()
numre = re.compile('^[\d,]+$')
rulere = re.compile('^(.*): (\d+)-(\d+) or (\d+)-(\d+)$')

myticket = None
myticket_scanning = True
othertickets = set()

with open( args.inputfile ) as inputfile:
    for line in inputfile:
        if line.strip() == '':
            continue
        if line.strip() == 'your ticket:':
            pass
        elif line.strip() == 'nearby tickets:':
            myticket_scanning = False
        elif numre.match( line.strip() ):
            numbers = [ int(x) for x in line.strip().split(',') ]
            if myticket_scanning is True:
                myticket = numbers
            else:
                othertickets.add( tuple(numbers) )
        else:
            match = rulere.match( line.strip() )
            if match:
                rules.add( tuple([ match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)) ]) )
            else:
                raise ValueError( "Cannot parse {}".format(line.strip() ) )

def match_number_against_rule ( number, rule ):
    return ( number >= rule[1] and number <= rule[2] ) or ( number >= rule[3] and number <= rule[4] )

# Which numbers in othertickets cannot satisfy *any* rule?
print( "Part 1:", len(othertickets), "other tickets" )
scanning_error_rate = 0
valid_tickets = set()
for ticket in othertickets:
    all_ticket_numbers_valid = True
    for number in ticket:
        number_valid_for_any_rule = False
        for rule in rules:
            if args.debug:
                print("Attempting to validate", number, "against", rule)
            if match_number_against_rule(number, rule):
                if args.debug:
                    print(number, "passes rule", rule[0])
                number_valid_for_any_rule = True
                break

        if not number_valid_for_any_rule:
            scanning_error_rate += number
            all_ticket_numbers_valid = False

    if all_ticket_numbers_valid:
        valid_tickets.add(ticket)

print("Scanning error rate", scanning_error_rate)

print( "Part 2:", len(valid_tickets), "valid tickets" )

# Now look at the numbers in order for all valid tickets, and find the one rule which satisies every nth number
potential_rules = []
for pos in range(len(myticket)):
    potential_rules.append( set() )
    if args.debug2:
        print("Testing all numbers in position", pos)
    for rule in rules:
        all_values_match_rule = True

        for ticket in valid_tickets:
            if not match_number_against_rule(ticket[pos], rule):
                if args.debug2:
                    print(pos, "th number on", ticket, "doesn't match", rule[0])
                all_values_match_rule = False
                break

        if all_values_match_rule:
            if args.debug2:
                print("Position", pos, "matches rule", rule[0])
            potential_rules[pos].add(rule[0])

# Collapse down our minimal rules, try to reach one rule per position
minimal = False
removed = set()
while not minimal:
    minimal = True
    to_remove = set()

    for pos in range(len(potential_rules)):
        prule = potential_rules[pos]
        if len(prule) > 1:
            minimal = False
        else:
            solo = next(iter(prule))
            if solo not in removed:
                if args.debug2:
                    print(pos, "can only be", solo)
                to_remove.add(solo)

    if not minimal and len(to_remove) == 0:
        print("Seem to have got stuck while optimising")
        exit(1)

    for item in to_remove:
        for prule in potential_rules:
            if len(prule) > 1:
                prule.discard(item)
        removed.add(item)

    # Try removing anything in to_remove from each potential rule which isn't a duplicate

# Now we can sort out our ticket
product = 1
for pos in range(len(myticket)):
    field = next(iter(potential_rules[pos]))
    if 'departure' in field:
        product *= myticket[pos]

print("Part 2 answer:", product)
