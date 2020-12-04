#!/usr/bin/perl

use strict;
use warnings;
use English;
use Data::Dumper;

# Input records are sepated by multiple newlines
our $INPUT_RECORD_SEPARATOR="\n\n";

my $num_valid = 0;
while (my $record = <>) {
  my %passport;
  # Each record is a multi-line string containing colon-separated key-value pairs
  while ( $record =~ m/(\S+):(\S+)/g ) {
    $passport{$1} = $2;
  }
  # We now have a key-value hash %passport

  my $valid = 1;
  foreach my $field ( qw/byr iyr eyr hgt hcl ecl pid/ ) {
    if ( not exists $passport{$field} ) {
      $valid = 0;
    }
  }

  if ( $valid ) {
    $num_valid++;
  }
}

print($num_valid, " valid passports\n")
