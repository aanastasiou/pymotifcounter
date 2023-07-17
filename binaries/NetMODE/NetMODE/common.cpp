#include "common.h"
using namespace std;

int int_ram_pt = 0;
int double_ram_pt = 0;
int HashNode_pt = 0; 
int verbose = 0;
int showall = 0;

//int	       int_ram_pool[MAXINTSIZE];
//double     double_ram_pool[MAXDOUBLESIZE];
//HashNode_t HashNodePool[1 << 16]; 

args_t::args_t()
{
	memset(this, 0, sizeof(args_t));
}

void args_t::pr()
{
	cout << "subgraph_size = " << subgraph_size << endl;
	cout << "graph_size = " << graph_size << endl;
	cout << "row_size = " << row_size << endl;
	cout << "edges = " << edges << endl;
	cout << "edge_offset = " << edge_offset << endl; 
	cout << "adj_mat = " << adj_mat << endl; 
	cout << "pattern = " << pattern << endl; 
	cout << "subgraph_ref = " << subgraph_ref << endl;
	cout << "hash_table = " << hash_table << endl;
	cout << "exception_id = " << exception_id << endl;
	cout << "exception_table = " << exception_table << endl; 
	//cout << "subgraph_count = " << subgraph_count << endl; 
	//cout << "subgraph_count_2 = " << subgraph_count_2 << endl; 
	//cout << "this_subgraph_count = " << this_subgraph_count << endl; 
	//cout << "origin_subgraph_count = " << origin_subgraph_count << endl; 
	cout << endl;
}

int *getIntMemSpace(int size)
{
	return new int[size];

    /*
	 *if (int_ram_pt + size <= MAXINTSIZE){
	 *    int *r = int_ram_pool + int_ram_pt;
	 *    int_ram_pt += size;
	 *    return r;
	 *}
	 *assert(false);
	 *puts("int_ram_pool has no more space");
	 *return 0;
     */
}

double *getDoubleMemSpace(int size)
{
	return new double[size];
    /*
	 *if (double_ram_pt + size <= MAXDOUBLESIZE){
	 *    double *r = double_ram_pool + double_ram_pt;
	 *    double_ram_pt += size;
	 *    return r;
	 *}
	 *puts("double_ram_pool has no more space");
	 *return 0;
     */
}

HashNode_t *getHashNode()
{
	return new HashNode_t;
    /*
	 *if (HashNode_pt >= (1 << 16)){
	 *    HashNode_pt = 0;
	 *    puts("HashNodePool has no more space");
	 *    return HashNodePool + (HashNode_pt ++);
	 *}
	 *return HashNodePool + (HashNode_pt ++);
     */
}

inline int readError(){
	fprintf(stderr, "Error occurs while reading. Please check input.\n\n");
	return -1;
}

int readData(args_t *arg)
{
	int &graph_size = arg->graph_size;
	int &row_size = arg->row_size;
	int &sizeof_edges = arg->sizeof_edges;
	int *&edges = arg->edges;
	int *&edge_offset = arg->edge_offset;
	int *&adj_mat = arg->adj_mat;

	vector< vector<int> > E_temp;

	scanf("%d", &graph_size);

	if (graph_size < 1) return readError();
	
	E_temp.resize(graph_size + 1);

	row_size = graph_size >> 5;
	if (graph_size & 31){
		++ row_size;
	}

	adj_mat = getIntMemSpace(row_size * (graph_size + 1) + 1);
	if (adj_mat == 0) return 2;
	edge_offset = getIntMemSpace(graph_size + 3);
	if (edge_offset == 0) return 2;

	//memset(adj_mat, 0, (row_size * (graph_size + 1) + 1) * sizeof(unsigned int)); //memset.h
	int i, j, t = row_size * (graph_size + 1) + 1;

	for (i = 0; i < t; ++ i){
		adj_mat[i] = 0;
	}

	int a, b, E_Sum = 0;
	while (scanf("%d %d", &a, &b) == 2){
		if (a < 1 || a > graph_size) return readError();
		if (b < 1 || b > graph_size) return readError();
		if (a == b) continue; // no loop
		if (!(adj_mat[a * row_size + (b >> 5)] & (1 << (b & 31)))){
			adj_mat[a * row_size + (b >> 5)] |= (1 << (b & 31));
			if (!(adj_mat[b * row_size + (a >> 5)] & (1 << (a & 31)))){
				E_temp[a].push_back(b);
				E_temp[b].push_back(a);
			}
		}
		++ E_Sum;
	}

	for (i = 1; i <= graph_size; ++ i){
		sort(E_temp[i].begin(), E_temp[i].end());
	}
	edge_offset[0] = 0;
	sizeof_edges = E_Sum * 2 + 10;
	edges = getIntMemSpace(sizeof_edges);
	E_temp[0].resize(0);

	for (i = 1; i <= graph_size; ++ i){
		edge_offset[i] = edge_offset[i - 1] + E_temp[i - 1].size();
		for (j = 0; j < (int)E_temp[i].size(); ++ j){
			edges[edge_offset[i] + j] = E_temp[i][j];
		}
	}
	edge_offset[graph_size + 1] = edge_offset[graph_size] + E_temp[graph_size].size();
	return 0;
}

string convertULLtoString(unsigned long long int number)
{
  if(number==0) {
    return "0";
  }
  string temp="";
  while(number>0) {
    temp="0123456789"[number%10]+temp;
    number/=10;
  }
  return temp;
}
