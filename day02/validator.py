#!/usr/bin/python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of passwords and rules")
args = parser.parse_args()

class Passwd:
  def __init__(self, string):
    pwrule = re.compile('^(?P<min>\d+)-(?P<max>\d+) (?P<char>\w): (?P<passwd>\w+)$')

    match = pwrule.match(string)
    if not match:
      raise ValueError("Failed to match line against password rule")

    self.min = int(match.group('min'))
    self.max = int(match.group('max'))
    self.char = match.group('char')
    self.passwd = match.group('passwd')

  def __str__(self):
    return('{} must contain between {} and {} instances of {}'.format (self.passwd, self.min, self.max, self.char))

  def valid(self):
    # count the instances of char in passwd
    chars = [x for x in self.passwd if x == self.char]
    return(self.min <= len(chars) <= self.max)

# Slurp integers from file into array
validpws = 0
inputfile = open( args.inputfile )
for line in inputfile:
  try:
    passwd = Passwd(line)
  except ValueError as err:
    print('{0}: {1}'.format(err, line.strip()))
    continue

  if passwd.valid():
    validpws += 1

print("{} valid passwords".format(validpws))
