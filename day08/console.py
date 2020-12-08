#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of code")
parser.add_argument("--part2",  action="store_true", help="Part 2: Funge instructions")
args = parser.parse_args()

# Slurp integers from file into array
program = []
inputfile = open( args.inputfile )
for line in inputfile:
  params = line.strip().split()
  program.append( tuple(( params[0], int(params[1]) )) )

def execute(program):
  pc = 0
  acc = 0
  seeninstrs = set()
  
  while True:
    if pc >= len(program):
      print("Reached end of program")
      print(acc)
      return True
  
    if pc in seeninstrs:
      print("We are repeating instruction", pc)
      print("Accumulator is", acc)
      return False
  
    seeninstrs.add(pc)
  
    inst = program[pc][0]
    param = program[pc][1]
  
    if inst == 'nop':
      pc += 1
    elif inst == 'acc':
      acc += param
      pc += 1
    elif inst == 'jmp':
      pc += param
    else:
      raise RuntimeError("Unknown instruction:", inst)
  
if not args.part2:
  execute(program)
else:
  for i in range( len(program) ):
    # Step over the program toggling nop and jmp
    if program[i][0] == 'nop' or program[i][0] == 'jmp':
      newprogram = program.copy()
      if program[i][0] == 'nop':
        newprogram[i] = tuple (( 'jmp', program[i][1] ))
      else:
        newprogram[i] = tuple (( 'nop', program[i][1] ))
      print("### Toggling instruction at", i)

      if execute(newprogram):
        break
