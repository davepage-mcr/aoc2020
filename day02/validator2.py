#!/usr/bin/python3

import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfile",  help="Input file of passwords and rules")
args = parser.parse_args()

class Passwd:
  def __init__(self, string):
    pwrule = re.compile('^(?P<posa>\d+)-(?P<posb>\d+) (?P<char>\w): (?P<passwd>\w+)$')

    match = pwrule.match(string)
    if not match:
      raise ValueError("Failed to match line against password rule")

    self.posa = int(match.group('posa'))
    self.posb = int(match.group('posb'))
    self.char = match.group('char')
    self.passwd = match.group('passwd')

  def __str__(self):
    return('{} must contain exactly one {} in positions {} or {}'.format (self.passwd, self.char, self.posa, self.posb))

  def valid(self):
    chara = self.passwd[self.posa-1]
    charb = self.passwd[self.posb-1]
    return ( (chara == self.char) ^ (charb == self.char) )

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
