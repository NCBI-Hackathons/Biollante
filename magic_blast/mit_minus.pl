#!/usr/bin/perl

my $p=1;
while(<>) { 
    $p=1 if (/^\>/);
    $p=0 if (/chloroplast/ || /mitochondria/);
    print if $p==1;
}
