#!/usr/bin/perl -w

use strict;

sub swap #(\input, idx a, idx b)
{
	my ($input, $idxA, $idxB) = @_;
	return if($idxA == $idxB);
	
	my $temp = $$input[$idxA];
	$$input[$idxA] = $$input[$idxB];
	$$input[$idxB] = $temp;
}

sub quicksort #(\input, idx left, idx right)
{
	my ($input, $left, $right) = @_;
	return 0 if($left >= $right);

	my $pivot = $$input[$left];
	my $i = $left + 1;
	my $j = $i;
	
	while($j <=$right)
	{
		if($pivot < $$input[$j])
		{
			$j++;
		}
		else
		{
			&swap($input, $i, $j);
			$i++;
			$j++;
		}
	}
	
	&swap($input, $i - 1, $left);
	
	#print "After partitioning,  on L=$left, R=$right, arr is ( " . join(",", @$input) . " )\n";
	
	my $comps = &quicksort($input, $left, $i - 2);
	$comps += &quicksort($input, $i, $right);
	
	return ($comps + $right - $left);
}

my @input;
while(<>)
{
	chomp;
	next unless (m/\S/);
	push(@input, $_);
}

print "Input size is " . scalar(@input) . "\n";

my $numComps = &quicksort(\@input,0,$#input);

print "Number of comparisions = " . $numComps . "\n";

# open OUTFILE, ">", "sorted.txt"
	# or die "Cannot open sorted.txt : $!";
# print OUTFILE "" . join("\n", @input) . "\n";
