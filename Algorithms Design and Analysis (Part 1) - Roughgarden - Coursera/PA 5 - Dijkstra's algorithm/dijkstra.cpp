#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cassert>
#include <heap.h>

using namespace std;

class NodeKey
{
public:
	size_t score;
	size_t node;
	
	NodeKey(size_t s, size_t n): score(s), node(n) {}
	NodeKey(): score(0), node(0) {}
	
	inline bool operator<(const NodeKey& rhs) const { return (score < rhs.score); }
	inline bool operator>(const NodeKey& rhs) const { return (score > rhs.score); }
	inline bool operator==(const NodeKey& rhs) const { return (score == rhs.score); }
	inline bool operator<=(const NodeKey& rhs) const { return (score <= rhs.score); }
	inline bool operator>=(const NodeKey& rhs) const { return (score >= rhs.score); }
};

class Edge
{
public:
	size_t dest;
	size_t weight;
	Edge():dest(0),weight(0) {}
	Edge(size_t a, size_t b):dest(a),weight(b) {}
};
typedef vector<Edge> EdgeList;
typedef vector<EdgeList> AdjList;

class Graph
{
private:
	AdjList m_adjList;
	size_t m_numNodes;
	size_t m_maxWeight;
	
public:
	Graph(istream& IN, size_t numNodes);
	void runDijkstra(size_t src, vector<size_t>& distances);
};

Graph::Graph(istream& IN, size_t numNodes):m_numNodes(numNodes), m_maxWeight(0)
{
	m_adjList.assign(numNodes+1, EdgeList());
	string line;
	size_t currNode = 0;
	
	while(getline(IN, line))
	{
		currNode++;
		size_t num1=0, num2=0, count=0;;
		char c = '\0';
		istringstream ISS(line);
		ISS >> num1;
		assert(num1 == currNode);
		
		while(ISS >> num1)
		{
			ISS >> c;
			assert(c == ',');
			ISS >> num2;
			m_adjList[currNode].push_back(Edge(num1, num2));
			if(num2 > m_maxWeight)
				m_maxWeight = num2;
			count++;
		}
		//cout << "Added " << count << " edges for node " << currNode << endl;
		assert(m_adjList[currNode].size() == count);
	}
}

void Graph::runDijkstra(size_t src, vector<size_t>& distances)
{
	distances.assign(m_numNodes+1, m_maxWeight*2);
	MinHeap<NodeKey> edgeHeap;
	size_t numExplored=0;
	vector<bool> explored(m_numNodes+1, false);
	explored[src] = true;
	numExplored++;
	distances[src] = 0;
	
	for(size_t i=0; i<m_adjList[src].size(); i++)
	{
		Edge& edge = m_adjList[src][i];
		edgeHeap.insert(NodeKey(edge.weight, edge.dest));
	}
	
	while(!edgeHeap.empty())
	{
		NodeKey nodekey = edgeHeap.extract_min();
		if(explored[nodekey.node])
			continue;
		explored[nodekey.node] = true;
		distances[nodekey.node] = nodekey.score;

		EdgeList& nEdges = m_adjList[nodekey.node];
		for(size_t i=0; i<nEdges.size(); i++)
		{
			Edge& edge = nEdges[i];
			if(explored[edge.dest])
				continue;
			size_t newScore = (distances[nodekey.node] + edge.weight);
			edgeHeap.insert(NodeKey(newScore, edge.dest));
		}
	}
}

int main(int argc, char* argv[])
{
	string numstr(argv[2]);
	istringstream ISS(numstr);
	size_t numNodes = 0;
	ISS >> numNodes;
	assert(numNodes > 0);
	
	ifstream IN(argv[1]);
	assert(IN);
	
	Graph graph(IN, numNodes);
	vector<size_t> distances;
	
	graph.runDijkstra(1, distances);
	
	cout << distances[7] << endl;
	cout << distances[37] << endl;
	cout << distances[59] << endl;
	cout << distances[82] << endl;
	cout << distances[99] << endl;
	cout << distances[115] << endl;
	cout << distances[133] << endl;
	cout << distances[165] << endl;
	cout << distances[188] << endl;
	cout << distances[197] << endl;
	
	
	//for(size_t i=0; i<distances.size(); i++)
	//{
	//	cout << "[" << i << "] " << distances[i] << endl;
	//}
	
	return 0;
}
