#include "common.h"
using namespace std;

namespace preProcess{
	int  global_i;
	int  VList[10];
	int  tr[10], *pat;
	int  patter_state;
	int  subgraph_size;
	bool graph_mat[10][10];//, visited[10];
}
using namespace preProcess;

inline int  graph2Bit();
inline int  getGlobal_i(int x);
inline void bit2Graph(int x);

void enumerateAut(); 

void generateSubgraph(int *pattern, int *&patternMap, int __subgraphSize, int &pattern_num)
{
	
	subgraph_size = __subgraphSize;
	pat = pattern;
	patter_state = 1 << (subgraph_size * subgraph_size);
	std::vector <int> pattern_tmp;
	
	int i, stat;

	for (stat = 1; stat < patter_state; ++ stat) pat[stat] = 0;
	pattern_num = 1;
	pattern_tmp.clear();
	
	for (stat = 1; stat < patter_state; ++ stat){
		if (pat[stat] != 0) continue;

		bit2Graph(stat);
		if (getGlobal_i(stat) == stat){
			global_i = pattern_num ++;
			pattern_tmp.push_back(stat);
		}
		else{
			global_i = -1;
		}

        /*
		 *for (j = 0; j < subgraph_size; ++ j){
		 *    visited[j] = false;
		 *}
         */
		enumerateAut();
	}
	//printf("pattern_num = %d\n", pattern_num);
	patternMap = getIntMemSpace(pattern_num + 3);
	for (i = 0; i < pattern_num; ++ i){
		patternMap[i + 1] = pattern_tmp[i];
	}
}

void bit2Graph(int x)
{
	int i, j;
	for (i = subgraph_size - 1; i >= 0; -- i){
		for (j = subgraph_size - 1; j >= 0; -- j){
			graph_mat[i][j] = x & 1;
			x >>= 1;
		}
	}
}

inline int graph2Bit(){
	int i, j, x = 0;
	for (i = 0; i < subgraph_size; ++ i){
		for (j = 0; j < subgraph_size; ++ j){
			x <<= 1;
			x |= (graph_mat[ tr[i] ][ tr[j] ] & 1);
		}
	}
	return x;
}

void enumerateAut()
{
	int i;
	for (i = 0; i < subgraph_size; ++ i){
		tr[i] = i;
	}
	do{
		pat[graph2Bit()] = global_i;
	}while (next_permutation(tr, tr + subgraph_size));
}

inline int getGlobal_i(int x){
	for (int i = 0; i < subgraph_size; ++ i){
		if (graph_mat[i][i]) return -1;
	}
	return x;
}

void handleExceptions(int *exception_id, ULL *exception_table)
{
	int exception_count = 18;
	ULL exceptions[] = {
		1162783744LL , 1292807168LL ,
		4850523168LL , 21493521440LL,
		26023442528LL, 30318278752LL,
		11494372448LL, 23850660960LL,
		11364349024LL, 15659185248LL,
		5957855792LL , 22600854064LL,
		13591459952LL, 30234458224LL, 
		24945504880LL, 33527050864LL,
		14682012272LL, 31325010544LL
	};

	int i, j, k, hCode, hTot = 0;
	ULL x, one64 = 1;
	for (k = 0; k < exception_count; ++ k){

		x = exceptions[k];
		hCode = exceptions[k] % EXCMOD;
		++ hTot;
		exception_id[hCode] = hTot;
		exception_table[hCode] = x;

		for (i = 5; i >= 0; -- i){
			for (j = 5; j >= 0; -- j){
				graph_mat[i][j] = x & 1;
				x >>= 1;
			}
		}
		for (i = 0; i < 6; ++ i){
			tr[i] = i;
		}
		while (next_permutation(tr, tr + 6)){
			x = 0;
			for (i = 0; i < 6; ++ i){
				for (j = 0; j < 6; ++ j){
					x <<= 1;
					if (graph_mat[ tr[i] ][ tr[j] ]){
						x |= one64;
					}
				}
			}
			hCode = x % EXCMOD;
			exception_id[hCode] = hTot;
			exception_table[hCode] = x;
		}
	}
}
