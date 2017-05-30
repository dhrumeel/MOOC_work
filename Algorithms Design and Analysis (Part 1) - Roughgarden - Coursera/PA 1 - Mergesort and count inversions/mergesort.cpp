#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

long sort_and_count_inversions(vector<unsigned int>& input, size_t first, size_t last, vector<unsigned int>& sorted)
{
  size_t len = (last - first);
  if(len == 0)
  {
    sorted.push_back(input[first]);
    return 0;
  }

  long numInversions = 0;
  size_t mid = (size_t)(len / 2);
  vector<unsigned int> left;
  vector<unsigned int> right;

  numInversions += sort_and_count_inversions(input, first, first+mid, left);
  numInversions += sort_and_count_inversions(input, first+mid+1, last, right);

  size_t lidx=0, ridx=0;

  //Merge
  for(size_t i=0; i<=len; i++)
  {
    if(lidx >= left.size())
    {
      sorted.insert(sorted.end(), right.begin()+ridx, right.end());
      break;
    }

    if(ridx >= right.size())
    {
      sorted.insert(sorted.end(), left.begin()+lidx, left.end());
      break;
    }

    if(left[lidx] < right[ridx])
    {
      sorted.push_back(left[lidx]);
      lidx++;
    }
    else
    {
      sorted.push_back(right[ridx]);
      ridx++;
      numInversions += (left.size() - lidx);
    }
  }

  return numInversions;
}

int main(int argc, char* argv[])
{
  long numInversions = 0;
  ifstream INFILE(argv[1], fstream::in);
  vector<unsigned int> input;

  while(INFILE.good())
  {
    int number = 0;
    INFILE >> number;
    if(number != 0)
      input.push_back(number);
  }

  cout << "Input size is " << input.size() << endl;

  vector<unsigned int> sorted;
  numInversions = sort_and_count_inversions(input, 0, input.size() - 1, sorted);

  cout << "Number of inversions is " << numInversions << endl;

}

