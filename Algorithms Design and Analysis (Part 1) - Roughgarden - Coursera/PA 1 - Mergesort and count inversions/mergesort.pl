#!/usr/bin/perl -w

use strict;

sub sort_and_count_inversions #(\array input, idx first, idx last, \array sorted)
{
	my ($input, $first, $last, $sorted) = @_;

	my $size = ($last - $first);
	if ($size == 0)
	{
		@$sorted = ($input->[$first]);
		return 0;
	}
	if ($size == 1)
	{
		if($input->[$first] < $input->[$last])
		{
			@$sorted = ($input->[$first], $input->[$last]);
			return 0;
		}
		else
		{
			@$sorted = ($input->[$last], $input->[$first]);
			return 1;
		}
	}
	
	@$sorted = ();
	my $inversions = 0;
	my $mid = int($size / 2);
	my $left = [];
	my $right = [];
	
	$inversions += &sort_and_count_inversions($input, $first, ($first + $mid), $left);
	$inversions += &sort_and_count_inversions($input, ($first + $mid + 1), $last, $right);

MERGE:	
	for my $n (0 .. $size)
	{
		if(@$left == 0)
		{
			push(@$sorted, @$right);
			last MERGE;
		}
		if(@$right == 0)
		{
			push(@$sorted, @$left);
			last MERGE;
		}
		
		if($left->[0] < $right->[0])
		{
			push(@$sorted, (shift @$left));
		}
		else
		{
			push(@$sorted, (shift @$right));
			$inversions += scalar(@$left);
		}
	}
	
	return $inversions;
}

my @nums;
my $numInversions = 0;

while(<>)
{
	chomp;
	next unless (m/\S/);
	push(@nums, $_);
}

my $size = scalar(@nums);
print "Size of input = $size\n";

my $sortedNums = [];
$numInversions = &sort_and_count_inversions(\@nums, 0, $#nums, $sortedNums);

print "Num. inversions = $numInversions\n";
