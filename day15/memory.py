#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("start",  help="Comma-separated integers")
parser.add_argument("--debug",    action='store_true')
parser.add_argument("--target",   type=int, default=2020, help='Find the target-th number spoken')
args = parser.parse_args()

lastsaid = {}
prev = None
prev_first = None
turn = 1

def add_num ( num, turn ):
    global lastsaid
    global prev
    global prev_first

    if num not in lastsaid:
        prev_first = True
        next_num = 0
        if args.debug:
            print("First time", num, "has been said")
    else:
        pref_first = False
        next_num = turn - lastsaid[ num ]
        if args.debug:
            print(num, "was said on turn", lastsaid[num], next_num, "turns ago")

    prev = num
    lastsaid[ num ] = turn

    return next_num

turn = 1
for num in args.start.split(','):
    print("## Turn", turn, "speaks", num)
    next_num = add_num(int(num), turn)
    turn += 1

for turn in range(turn, args.target+1):
    print("## Turn", turn, "speaks", next_num)
    next_num = add_num(next_num, turn)
