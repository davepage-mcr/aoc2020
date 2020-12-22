#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of sums")
parser.add_argument("--debug",    action='store_true', help="Debug")
parser.add_argument("--part2",    action='store_true', help="Part 2: + before *")
args = parser.parse_args()

def tokenise( atoms ):
    # I'm trying not to Perl out and do this with regex!

    tokens = []
    nextvalueisexpectedresult = False
    expect = None

    for atom in atoms:
        if atom == '+' or atom == '*':
            tokens.append(atom)
        elif atom == '=':
            # Our next value must be an integer returned as the expected value
            nextvalueisexpectedresult = True
        elif atom[0] == '(':
            # We have at least one opening indentation
            if len(atom) == 1:
                tokens.append('(')
            else:
                ( recurse, throwaway ) = tokenise( [ atom[0], atom[1:] ] )
                tokens.extend( recurse )
        elif atom[-1] == ')':
            if len(atom) == 1:
                tokens.append(atom[0])
            else:
                ( recurse, throwaway ) = tokenise( [ atom[:-1], atom[-1] ] )
                tokens.extend( recurse )
        else:
            token = int(atom)
            if nextvalueisexpectedresult == True:
                expect = token
            else:
                tokens.append(token)

            # raise ValueError("Cannot tokenize atom {}".format(atom))

    return(tokens, expect)

def tokenstring(foo):
    return ' '.join( str(x) for x in foo )

def calc( tokens ):
    # First off, we handle parentheses

    if args.debug:
        print("Calculating", tokenstring(tokens))

    newtokens = []

    # Can't use a range iterator here as we may skip ahead
    i = 0
    while i < len(tokens):
        if tokens[i] == '(':
            nested = 0
            for j in range(i+1, len(tokens)):
                if tokens[j] == '(':
                    nested += 1
                elif tokens[j] == ')':
                    if nested > 0:
                        nested -= 1
                    else:
                        break
            if args.debug:
                print("We can treat", tokens[i+1:j], "as separate calc")
            result = calc( tokens[i+1:j] )
            newtokens.append(result)
            i = j+1
        else:
            newtokens.append(tokens[i])
            i += 1

    if args.part2:
        return part2calc(newtokens)
    else:
        return simplecalc(newtokens)

def simplecalc( tokens ):
    # We should have no parens here
    result = None

    # Just look at first 3 tokens which should be an operator and two numbers
    if tokens[1] == '+':
        result = tokens[0] + tokens[2]
    elif tokens[1] == '*':
        result = tokens[0] * tokens[2]

    if len(tokens) == 3:
        return(result)
    else:
        newtokens = [ result ]
        newtokens.extend( tokens[3:] )
        return simplecalc(newtokens)

def part2calc( tokens ):
    # Look for any additions and deal with them first
    if args.debug:
        print("Part 2 calc:", tokens)
    for i in range(len(tokens)):
        if tokens[i] == '+':
            result = tokens[i-1] + tokens[i+1]
            if len(tokens) == 3:
                return(result)
            else:
                newtokens = []
                if i - 1 > 0: # We're not at the start of our token list
                    newtokens.extend( tokens[0:i-1] )
                newtokens.append(result)
                if i + 1 < len(tokens): # We're not at the end of our token list
                    newtokens.extend( tokens[i+2:] )
                return(part2calc(newtokens))
    return simplecalc(tokens)

resultsum = 0

with open( args.inputfile ) as inputfile:
    for line in inputfile:
        (tokens, expect) = tokenise( line.strip().split() )
        if args.debug:
            print("### New calc:", tokenstring(tokens))
        result = calc(tokens)
        if expect != None:
            if result != expect:
                raise ValueError('Calculation of {} returns {} not expected {}'.format( tokenstring(tokens), result, expect))
            else:
                print("{} gives expected result {}".format(tokenstring(tokens), result))
        resultsum += result

print("Sum of results:", resultsum)
