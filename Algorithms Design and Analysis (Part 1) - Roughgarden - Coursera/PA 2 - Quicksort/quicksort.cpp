#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

inline void swap(vector<unsigned int>& input, size_t idx1, size_t idx2)
{
	if(idx1 != idx2)
	{
		unsigned int temp = input[idx1];
		input[idx1] = input[idx2];
		input[idx2] = temp;
	}
	return;
}

inline size_t medianOf3(vector<unsigned int>& input, size_t idxA, size_t idxB, size_t idxC)
{
	unsigned int A = input[idxA], B = input[idxB], C = input[idxC];
	if(A > B)
	{
		if(A > C)
		{	// A > B and A > C
			return((B > C) ? idxB : idxC);
		}
		else
		{	// A > B and C > A
			return idxA;
		}
	}
	else
	{
		if(B > C)
		{	// B > A and B > C
			return((A > C) ? idxA : idxC);
		}
		else
		{	// B > A and C > B
			return idxB;
		}
	}
}

unsigned long long qsort(vector<unsigned int>& input, size_t first, size_t last)
{
	unsigned long long comps = 0;
	size_t len = (last - first + 1);
	if(len <= 1)
	{
		return 0;
	}
	
	//Choose pivot
    size_t medianIdx = medianOf3(input, first, first + (size_t)((last-first)/2), last);
	swap(input, first, medianIdx);
	size_t pivotIdx = first;
	
	//Partition
	unsigned int pivot = input[pivotIdx];
	size_t i=first+1, j=first+1;
	while(j <= last)
	{
		if(input[j] < pivot)
		{
			swap(input, i, j);
			i++;
			j++;
		}
		else
		{
			j++;
		}
	}
	swap(input, pivotIdx, i-1);
	
	comps += (len - 1);

	comps += qsort(input, first, i-2);
	comps += qsort(input, i, last);
	
	return comps;
}

int main(int argc, char* argv[])
{
	ifstream INFILE(argv[1], fstream::in);
	vector<unsigned int> input;
	
	while(INFILE.good())
	{
		unsigned int number = 0;
		INFILE >> number;
		if(number != 0)
			input.push_back(number);
	}
	INFILE.close();
	
	cout << "Size of input is " << input.size() << endl;
	vector<unsigned int> sorted;
	
	unsigned long long comps = qsort(input, 0, input.size() - 1);
	
	cout << comps << " comparisons were made" << endl;

	// ofstream OUT("out.txt", fstream::out);
	// for(vector<unsigned int>::iterator it = input.begin(); it != input.end(); it++)
	// {
	  // OUT << *it << endl;
	// } 
	
	return 0;
}
