#!/usr/bin/env python3

import sys
import argparse
from itertools import combinations

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of ingredient lists")
parser.add_argument("--debug",    action='store_true', help="Debug")
args = parser.parse_args()

player = None

playerdecks = {}

with open( args.inputfile ) as inputfile:
    for line in inputfile:
        if line[0:6] == 'Player':
            player = int(line[7:-2])
            playerdecks[player] = []
        elif line.strip() == '':
            continue
        else:
            playerdecks[player].append(int(line))

deckempty = False
roundnum = 1
while not deckempty and roundnum < 1000:
    print("\n-- Round {} --".format(roundnum))
    plays = {}
    for player, deck in playerdecks.items(): 
        print("Player {}'s deck: {}".format(player, deck))
        play = deck.pop(0)
        plays[player] = play
        print("Player {} plays: {}".format(player, play))

    maxcard = None
    maxplayer = None
    playedcards = []

    for player, card in plays.items():
        playedcards.append(card)
        if maxcard == None or card > maxcard:
            maxcard = card
            maxplayer = player
    print("Player {} wins the round with {}!".format(maxplayer,maxcard))
    playedcards.sort(reverse=True)
    playerdecks[maxplayer].extend(playedcards)

    for player, deck in playerdecks.items():
        if len(deck) == 0:
            print("Player {} is out of cards!".format(player))
            deckempty = True

    roundnum += 1

print("\n== Post-game results ==")
for player, deck in playerdecks.items():
    score = 0
    for i in range(1, len(deck)+1):
        score += i * deck[-i]
    print("Player {}'s deck scores {}: {}".format(player, score, deck))
