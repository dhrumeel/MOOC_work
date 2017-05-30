#include <fstream>
#include <heap.h>
#include <iostream>
#include <cassert>

using namespace std;

int main(int argc, char* argv[])
{
	ifstream IN(argv[1]);
	assert(IN);
	
	MinHeap<size_t> large;
	MaxHeap<size_t> small;
	
	size_t num=0;
	IN >> num;
	size_t median = num;
	size_t sum = num;
	small.insert(num);
	
	cout << "Read " << num << endl;
	
	while(IN >> num)
	{
		//cout << "Read " << num << endl;
		if(num < median)
		{
			small.insert(num);
			if(small.size() > (large.size()+1))
				large.insert( small.extract_max() );
		}
		else
		{
			large.insert(num);
			if(large.size() > (small.size()+1))
				small.insert( large.extract_min() );
		}
		median = ( large.size() > small.size() ) ? large.report_min() : small.report_max();
		sum += median;
	}
	
	cout << "Sum = " << sum << endl;
	return 0;
}
