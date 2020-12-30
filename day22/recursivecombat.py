#!/usr/bin/env python3

import sys
import argparse
from itertools import combinations

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of ingredient lists")
parser.add_argument("--debug",    action='store_true', help="Debug")
args = parser.parse_args()

playerdecks = {}
nextgame = 1

with open( args.inputfile ) as inputfile:
    player = None
    for line in inputfile:
        if line[0:6] == 'Player':
            player = int(line[7:-2])
            playerdecks[player] = []
        elif line.strip() == '':
            continue
        else:
            playerdecks[player].append(int(line))

def recursivecombat( game, decks ):
    global nextgame
    seendecks = set()
    print("=== Game {:d} ===".format(game))
    nextgame += 1

    roundnum = 1
    while roundnum < 10000:
        print("\n-- Round {} (Game {}) --".format(roundnum, game))

        # Create an immutable representation of decks, as a tuple of tuples
        allcards = []
        for player in sorted(decks.keys()):
            cards = tuple(decks[player])
            allcards.append(cards)
        allcards = tuple(allcards)

        # Have we seen these decks before?
        if args.debug:
            print("At this point we have seen these decks:")
            for deck in seendecks:
                print("\t", deck)
            print("This deck is", allcards)

        if allcards in seendecks:
            # Player 1 wins the game
            print("We have already seen this configuration of cards!")
            print("The winner of game {} is player 1!".format(game))
            return(1, decks)
        else:
            seendecks.add(allcards)

        maxplayed = None
        maxplayer = None
        allplayed = {}
        recurse = True

        # Each player draws the top card
        emptydeck = False
        for player, deck in decks.items():
            print("Player {}'s deck: {}".format(player, deck))
            played = deck.pop(0)
            allplayed[player] = played

            # Has this player now run out of cards?
            if len(deck) == 0:
                if args.debug:
                    print("Player {} is now out of cards".format(player))
                emptydeck = True

            if maxplayed == None or played > maxplayed:
                maxplayed = played
                maxplayer = player

            if args.debug:
                print("Player {} plays: {}, has {} cards left".format(player, played, len(deck)))
            else:
                print("Player {} plays: {}".format(player, played))
            if len(deck) < played:
                if args.debug:
                    print("Player {} does not have enough cards to recurse".format(player))
                recurse = False

        if not recurse:
            woncards = sorted(allplayed.values(), reverse=True)
            if args.debug:
                print("Player {} wins round {} of game {} with {}; wins {}".format(maxplayer, roundnum, game, maxplayed, woncards ))
            else:
                print("Player {} wins round {} of game {}!".format(maxplayer, roundnum, game))
            decks[maxplayer].extend( woncards )

            if emptydeck:
                print("The winner of game {} is player {}!".format(game, maxplayer))
                return(maxplayer, decks)

        else:
            print("Playing a sub-game to determine the winner...")

            # Create new decks for each player consisting of copies of the next N cards in their hand
            # Where N is the value of the card they just played

            newdecks = {}
            for player, deck in decks.items():
                if args.debug:
                    print("Need to copy the top {} cards from {}: {}".format(allplayed[player], deck, deck[:allplayed[player]] ))
                newdecks[player] = deck[:allplayed[player]]
            print()
            subwinner, dontcare = recursivecombat( nextgame, newdecks )
            print("\n... anyway, back to game {}.".format(game))
           
            woncards = []
            for player, card in allplayed.items():
                if player != subwinner:
                   woncards.append(card)
            woncards = [ allplayed[subwinner] ] + woncards

            if args.debug:
                print("Player {} wins round {} of game {}; wins {}".format(subwinner, roundnum, game, woncards))
            else:
                print("Player {} wins round {} of game {}!".format(subwinner, roundnum, game))
            decks[subwinner].extend( woncards )

        roundnum += 1

    raise IndexError("This game took more than {} rounds, aborting".format(roundnum))

winner, playerdecks = recursivecombat(nextgame, playerdecks)

print("\n== Post-game results ==")
for player, deck in playerdecks.items():
    score = 0
    for i in range(1, len(deck)+1):
        score += i * deck[-i]
    print("Player {}'s deck scores {}: {}".format(player, score, deck))
