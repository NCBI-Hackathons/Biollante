#!/usr/bin/perl

my $i=1;
my $line=<>;
chomp($line);
@plants=split(/,/,$line);
shift(@plants);
while(<>) {
	chomp;
	my $j=0;
	my @fields=split(/,/,$_);
	shift(@fields);
	foreach(@fields) {
		print">$plants[$j]_$i\n$fields[$j]\n";
		$j++;
	}
	$i++;
}
