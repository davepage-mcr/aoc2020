#!/usr/bin/python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of answers")
parser.add_argument("--part2", action='store_true', help="Only count questions everyone in group has answered")
args = parser.parse_args()

def process_part2(lganswers):
    # Return the size of the set of questions *everybody* in the group answered
    possibleanswers = set([ x for x in 'abcdefghijklmnopqrstuvwxzy' ])
    for lanswers in lganswers:
        # print("Answers not yet skipped by anybody in group:", possibleanswers)
        # print("Next group member's answers:", lanswers)
        answers_to_remove = [] # Can't edit set while iterating over it
        for panswer in possibleanswers:
            if panswer not in lanswers:
                answers_to_remove.append(panswer)
        for atr in answers_to_remove:
            possibleanswers.discard(atr)

    print("Everyone in this group answered", len(possibleanswers), possibleanswers)
    return len(possibleanswers)                

def process( lganswers ):
    # Return the size of the set of questions *anybody* in the group answered
    if args.part2:
        return process_part2(lganswers)

    # lganswers is a list of sets
    lgroupset = set()
    for answers in lganswers:
        lgroupset |= answers

    return len(lgroupset)

total = 0

groupanswers = []
inputfile = open( args.inputfile )
for line in inputfile:
    line = line.strip();
    answers = set()
    if len(line) > 0:
        for char in line:
            answers.add(char)
        groupanswers.append(answers)
    else:
        total += process(groupanswers)
        groupanswers = []

# Catch termination by EOF not newline
total += process(groupanswers)
groupanswers = []

print(total)
