#!/usr/bin/perl -w

use strict;

my $successCount = 0;
my %nums;

while(<>)
{
	chomp;
	next unless (m/\S/);
	my ($num) = (m/(\d+)/);
	$nums{$num} = 1 if ($num <= 4000);
}

TARGET:
foreach my $target (2500 .. 4000)
{
	KEY:
	foreach my $num1 (keys %nums)
	{
		next KEY if($num1 > $target);
		my $diff = ($target - $num1);
		if(($num1 != $diff) and exists $nums{$diff})
		{
			$successCount++;
			#print "$target = $num1 + $diff\n";
			next TARGET;
		}
	}
}

print "Success count is " . $successCount . "\n";
