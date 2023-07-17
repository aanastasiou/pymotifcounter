#define DEBUG

#ifndef common_h
#define common_h

#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <cmath>
#include <set>
#define SQR(x) ((x) * (x))

typedef long long LL;
typedef unsigned long long ULL;
typedef unsigned int uint;

extern int verbose;
extern int showall;

using namespace std;

struct Tup6_t{
	int elem[6];
};

struct HashNode_t{
	int num;
	HashNode_t *next;
};

typedef HashNode_t* HashLink_t;

const int EXCMOD = 7045650; 
const int MAXINTSIZE = 1 << 25;
const int MAXHASHSIZE = 1 << 24;
const int MAXDOUBLESIZE = 1 << 20; 
const int MAXCLASSNUMOF6 = 10000000; 

extern HashNode_t HashNodePool[1 << 16]; 
extern double double_ram_pool[MAXDOUBLESIZE];
extern int int_ram_pool[MAXINTSIZE];

extern int int_ram_pt;
extern int double_ram_pt;
extern int HashNode_pt; 

int *getIntMemSpace(int size);
double *getDoubleMemSpace(int size);
HashNode_t *getHashNode(); 

void generateSubgraph(int *pattern, int *&patter_map, int subgraph_size, int &patNum);
void handleExceptions(int *excHash, ULL *exception_table);
void genRandomGraph(const int graph_size, const int row_size, int NumOfExchange, int *edges, int *edge_offset, int *adj_mat, int switch_para); 

struct args_t 
{ 
	int vacancy_num;
	bool *vacancy;
	
	int subgraph_size;
	int graph_size;
	int row_size;
	int sizeof_edges;
	
	int *edges;
	int *edge_offset; 
	int *adj_mat;

	int *pattern;
	int pattern_num;
		
	double origin_subgraph_sum;
	
	Tup6_t *subgraph_ref;
	HashLink_t *hash_table;
	int *exception_id;
	ULL *exception_table;

	ULL* subgraph_count; 
	ULL* subgraph_count_2; 
	ULL* this_subgraph_count; 
	vector<ULL> origin_subgraph_count; 
	
	int* subgraph_p_value;
	int* subgraph_cp_value;
	
	double *subgraph_concentration;
	double *subgraph_concentration_2;
	
	args_t();

	void pr();

};

int  readData(args_t *arg); 
void* kavoshSearch345(void *darg);
void *searchRandGraph345(void *arg);

void *kavoshSearch6(void *arg);
void *searchRandGraph6(void *arg);

string convertULLtoString(unsigned long long int number);
#endif // common_h
