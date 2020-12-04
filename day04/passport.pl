#!/usr/bin/perl

use strict;
use warnings;
use English;
use Data::Dumper;
use Getopt::Long;

my $part2;
GetOptions(
  "part2" => \$part2,
) or die ("Failed to parse command-line args");

# Input records are sepated by multiple newlines
our $INPUT_RECORD_SEPARATOR="\n\n";

sub valid_part1 {
  my %lpassport = @_;
  my $valid = 1;

  foreach my $field ( qw/byr iyr eyr hgt hcl ecl pid/ ) {
    if ( not exists $lpassport{$field} ) {
      $valid = 0;
    }
  }

  return $valid;
}

sub valid_part2 {
  my %lpassport = @_;

  ## Check valid years
  if ( not exists $lpassport{'byr'} or $lpassport{'byr'} !~ m/^\d{4}$/ or
        $lpassport{'byr'} < 1920 or $lpassport{'byr'} > 2002 ) {
    return 0;
  }
  elsif ( not exists $lpassport{'iyr'} or $lpassport{'iyr'} !~ m/^\d{4}$/ or
        $lpassport{'iyr'} < 2010 or $lpassport{'iyr'} > 2020 ) {
    return 0;
  }
  elsif ( not exists $lpassport{'eyr'} or $lpassport{'eyr'} !~ m/^\d{4}$/ or
        $lpassport{'eyr'} < 2020 or $lpassport{'eyr'} > 2030 ) {
    return 0;
  }


  ## Check valid height
  if ( not exists $lpassport{'hgt'} ) {
    return 0;
  }
  if ( $lpassport{'hgt'} !~ m/^(\d+)(cm|in)$/ ) {
    return 0;
  }
  if ( $2 eq 'cm' ) {
        if ( $1 < 150 or $1 > 193 ) {
          return 0;
        }
  } elsif ( $1 < 59 or $1 > 76 ) {
        return 0;
  }

  ## Check hair colour
  return 0
    if ( not exists $lpassport{'hcl'} or $lpassport{'hcl'} !~ m|^#[[:xdigit:]]{6}$| );

  ## Check eye colour
  return 0
    if ( not exists $lpassport{'ecl'} or $lpassport{'ecl'} !~ m/^(amb|blu|brn|gry|grn|hzl|oth)$/ );

  ## Check pid
  return 0
    if ( not exists $lpassport{'pid'} or $lpassport{'pid'} !~ m/^\d{9}$/ );

  ## Do not check cid
  return 1;
}

my $num_valid = 0;
while (my $record = <>) {
  my %passport;
  # Each record is a multi-line string containing colon-separated key-value pairs
  while ( $record =~ m/(\S+):(\S+)/g ) {
    $passport{$1} = $2;
  }
  # We now have a key-value hash %passport

  if ( $part2 ) {
    $num_valid++ if valid_part2(%passport)
  } else {
    $num_valid++ if valid_part1(%passport)
  }
}

print($num_valid, " valid passports\n");
