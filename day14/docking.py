#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of instructions")
parser.add_argument("--debug",    action='store_true')
parser.add_argument("--part2",    action='store_true', help="")
args = parser.parse_args()

mem = {}

def set_masks(mask):
    if args.debug:
        print("set_mask:", mask)

    # To set a bit to 1, OR it with 1
    # Create a mask where all the 0s and Xs are 0
    mask_zeroes = int( val.replace('X', '0'), 2 )
    if args.debug:
        print( "\tNew mask to set 0s:", bin(mask_zeroes) )

    # To set a bit to 0, AND it with 0
    # Create a mask where all the 1s and Xs are 1
    mask_ones = int( val.replace('X', '1'), 2 )
    if args.debug:
        print( "\tNew mask to set 1s:", bin(mask_ones) )

    return( mask_zeroes, mask_ones )

def set_val(val, mask_zeroes, mask_ones):

    if args.debug:
        print("Set\t{:8d} {}".format( val, bin(val)))
    masked_val = ( val | mask_zeroes ) & mask_ones
    if args.debug:
        print("Setting\t{:8d} {}".format( masked_val, bin(masked_val)))

    return( masked_val )

def mask_addr(laddr, lmask):
    if args.debug:
        print("Masking address", laddr)

    baddr = "{:036b}".format(laddr)
    maddr = ''

    for i in range(len(baddr)):
        if lmask[i] == '0':
            maddr += baddr[i]
        else:
            maddr += lmask[i]

    if args.debug:
        print("Masked address is", maddr)
    return(maddr)

def set_masked_addr(laddr, lval):
    global mem

    if ( 'X' in laddr ):
        set_masked_addr( laddr.replace('X', '0', 1), lval )
        set_masked_addr( laddr.replace('X', '1', 1), lval )
        return

    if args.debug:
        print("Setting", laddr, "to", lval)

    mem[ int(laddr, 2) ] = lval

with open( args.inputfile ) as inputfile:
    for line in inputfile:
        [cmd, val] = line.strip().split(' = ')

        if cmd == 'mask':
            if args.part2:
                mask = val
            else:
                [mask_zeroes, mask_ones] = set_masks(val)
        elif cmd[0:3] == 'mem':
            addr = int(cmd[4:-1])
            if args.part2:
                masked_addr = mask_addr(addr, mask)
                set_masked_addr(masked_addr, int(val))
            else:
                mem[addr] = set_val(int(val), mask_zeroes, mask_ones)
        else:
            raise ValueError("Unrecognised command {}".format(cmd))

total = 0
for memory in mem.values():
    total += memory
print("Total in memory:", total)
