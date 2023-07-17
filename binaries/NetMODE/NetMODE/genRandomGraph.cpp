#include "common.h"
#include <algorithm>
using namespace std;

const char switches[16] = {15, 2, 2, 2,  2, 6, 6, 2,  2, 6, 6, 2,  14, 2, 2, 14};

vector < set<int> > directed_edges, undirected_edges;
int *bidirected_vertex, *directed_vertex_in, *directed_vertex_out;
int bidirected_vertex_num, directed_vertex_num;

bool needInit = true;

bool bidirected_vertex_shuffle(int *adjMat, int row_size){
	random_shuffle(bidirected_vertex, bidirected_vertex + (bidirected_vertex_num << 1));
	int i, vertex1, vertex2;
	for (i = 0; i < bidirected_vertex_num; ++ i){
		vertex1 = bidirected_vertex[i << 1];
		vertex2 = bidirected_vertex[(i << 1) + 1];
		if (vertex1 == vertex2){
			return false;
		}
		if (adjMat[vertex1 * row_size + (vertex2 >> 5)] & (1 << (vertex2 & 31))){
			return false;
		}
		if (adjMat[vertex2 * row_size + (vertex1 >> 5)] & (1 << (vertex1 & 31))){
			return false;
		}
		adjMat[vertex1 * row_size + (vertex2 >> 5)] |= (1 << (vertex2 & 31));
		adjMat[vertex2 * row_size + (vertex1 >> 5)] |= (1 << (vertex1 & 31));
	}
	return true;
}

bool directed_vertex_shuffle(int *adjMat, int row_size){
	random_shuffle(directed_vertex_out, directed_vertex_out + directed_vertex_num);
	int i, vertex_in, vertex_out;
	for (i = 0; i < directed_vertex_num; ++ i){
		vertex_in = directed_vertex_in[i];
		vertex_out = directed_vertex_out[i];
		if (vertex_in == vertex_out){
			return false;
		}
		if (adjMat[vertex_out * row_size + (vertex_in >> 5)] & (1 << (vertex_in & 31))){
			return false;
		}
		if (adjMat[vertex_in * row_size + (vertex_out >> 5)] & (1 << (vertex_out & 31))){
			return false;
		}
		adjMat[vertex_in * row_size + (vertex_out >> 5)] |= (1 << (vertex_out & 31));
	}
	return true;
}

void genRandomGraph(const int nV, const int row_size, \
				int NumOfExchange, int *edges, int *edge_offset, int *adjMat, int switch_para)
{
	int i, j, k, succ = 0;
	int a, b, c, d, p, q, c_ind, d_ind;
	int E_Sum, v;
	int switch_type;
	//int ReplaceQueue[5][3];
	
	set <int>::iterator pSet;
	if (needInit && (switch_para < 16)){
		needInit = false;
		
		directed_edges.resize(nV + 1);
		undirected_edges.resize(nV + 1);
		for (i = 0; i <= nV; ++ i){
			directed_edges[i].clear();
			undirected_edges[i].clear();
		}
		
		for (i = 1; i <= nV; ++ i){
			for (j = edge_offset[i]; j < edge_offset[i + 1]; ++ j){
				v = edges[j];
				if (adjMat[i * row_size + (v >> 5)] & (1 << (v & 31))){
					directed_edges[i].insert(v);
				}
				undirected_edges[i].insert(v);
			}
		}
	}
	
	if (needInit && (switch_para == 16)){
		needInit = false;

		undirected_edges.resize(nV + 1);
		
		bidirected_vertex = new int[(edge_offset[nV + 1] + 1) << 1];
		directed_vertex_in  = new int[(edge_offset[nV + 1] + 1)];  
		directed_vertex_out = new int[(edge_offset[nV + 1] + 1)]; 
		
		bidirected_vertex_num = 0;
		directed_vertex_num = 0;
		
		bool i2v, v2i;
		for (i = 1; i <= nV; ++ i){
			for (j = edge_offset[i]; j < edge_offset[i + 1]; ++ j){
				v = edges[j];
				
				i2v = (adjMat[i * row_size + (v >> 5)] & (1 << (v & 31))) != 0;
				v2i = (adjMat[v * row_size + (i >> 5)] & (1 << (i & 31))) != 0;
				
				if (v2i && i2v && i < v){
					bidirected_vertex[(bidirected_vertex_num << 1)]     = i;
					bidirected_vertex[(bidirected_vertex_num << 1) + 1] = v;
					++ bidirected_vertex_num;
				}
				
				if (i2v && (!v2i)){
					directed_vertex_in [directed_vertex_num] = i;
					directed_vertex_out[directed_vertex_num] = v;
					++ directed_vertex_num;
				}
			}
		}
	}
	
	if (switch_para != 16){
		for (i = 0; i < NumOfExchange; ++ i){
			for (a = 1; a <= nV; ++ a){
				if (directed_edges[a].empty()) continue;
				do {
					b = (rand() % nV) + 1;
				} while (a == b);
				if (directed_edges[b].empty()) continue;
				
				switch_type = 0;
				p = q = -1;
				for (j = 0; j < NumOfExchange; ++ j) {
					c_ind = rand() % directed_edges[a].size();
					for (pSet = directed_edges[a].begin(), k = 0; k < c_ind; ++ k, ++ pSet);
					c = *pSet;
					if (c == b) continue;
					if ( adjMat[b * row_size + (c >> 5)] & (1 << (c & 31))) continue;
					if ( adjMat[c * row_size + (a >> 5)] & (1 << (a & 31))) switch_type += 4;
					if ( adjMat[c * row_size + (b >> 5)] & (1 << (b & 31))) switch_type += 2;
					p = c_ind;
					break;
				}

				if (p == -1) continue;

				for (j = 0; j < NumOfExchange; ++ j) {
					d_ind = rand() % directed_edges[b].size();
					for (pSet = directed_edges[b].begin(), k = 0; k < d_ind; ++ k, ++ pSet);
					d = *pSet;
					if (d == a) continue;
					if ( adjMat[a * row_size + (d >> 5)] & (1 << (d & 31))) continue;
					if ( adjMat[d * row_size + (a >> 5)] & (1 << (a & 31))) switch_type += 1;
					if ( adjMat[d * row_size + (b >> 5)] & (1 << (b & 31))) switch_type += 8;
					q = d_ind;
					break;
				}

				if (q == -1) continue;
				
				if ((switches[switch_type] & switch_para) == 0) continue;
				
				if (((switch_para & 12) != 0) && (switch_type == 12)){
					directed_edges[a].erase(c);
					directed_edges[a].insert(d);
					directed_edges[b].erase(d);
					directed_edges[b].insert(c);
					
					directed_edges[c].erase(a);
					directed_edges[c].insert(b);
					directed_edges[d].erase(b);
					directed_edges[d].insert(a);
					
					adjMat[a * row_size + (c >> 5)] &= (~(1 << (c & 31)));
					adjMat[a * row_size + (d >> 5)] |= (1 << (d & 31));
					adjMat[b * row_size + (d >> 5)] &= (~(1 << (d & 31)));
					adjMat[b * row_size + (c >> 5)] |= (1 << (c & 31));
					
					adjMat[c * row_size + (a >> 5)] &= (~(1 << (a & 31)));
					adjMat[c * row_size + (b >> 5)] |= (1 << (b & 31));
					adjMat[d * row_size + (b >> 5)] &= (~(1 << (b & 31)));
					adjMat[d * row_size + (a >> 5)] |= (1 << (a & 31));


					undirected_edges[a].insert(d);
					undirected_edges[d].insert(a);
					undirected_edges[b].insert(c);
					undirected_edges[c].insert(b);

					undirected_edges[a].erase(c);
					undirected_edges[c].erase(a);
					undirected_edges[b].erase(d);
					undirected_edges[d].erase(b);
				}
				else{
					
					directed_edges[a].erase(c);
					directed_edges[a].insert(d);
					directed_edges[b].erase(d);
					directed_edges[b].insert(c);
					
					adjMat[a * row_size + (c >> 5)] &= (~(1 << (c & 31)));
					adjMat[a * row_size + (d >> 5)] |= (1 << (d & 31));
					adjMat[b * row_size + (d >> 5)] &= (~(1 << (d & 31)));
					adjMat[b * row_size + (c >> 5)] |= (1 << (c & 31));


					undirected_edges[a].insert(d);
					undirected_edges[d].insert(a);
					undirected_edges[b].insert(c);
					undirected_edges[c].insert(b);
					if (!(switch_type & 4)){
						undirected_edges[a].erase(c);
						undirected_edges[c].erase(a);
					}
					if (!(switch_type & 8)){
						undirected_edges[b].erase(d);
						undirected_edges[d].erase(b);
					}
				}
				++ succ;
			}
		}
		//fprintf(stderr, "edge swap success #: %d\n", succ);
	}
	
	
	if (switch_para == 16){
		if (bidirected_vertex_num  <= (directed_vertex_num << 1)){
			do{
				do{
					memset(adjMat, 0, sizeof(int) * (row_size * (nV + 1) + 1));
				}while(!bidirected_vertex_shuffle(adjMat, row_size));
			}while(!directed_vertex_shuffle(adjMat, row_size));
		}
		else{
			do{
				do{
					memset(adjMat, 0, sizeof(int) * (row_size * (nV + 1) + 1));
				}while(!directed_vertex_shuffle(adjMat, row_size));
			}while(!bidirected_vertex_shuffle(adjMat, row_size));
		}
		for (i = 1; i <= nV; ++ i){
			undirected_edges[i].clear();
		}
		for (i = 0; i < bidirected_vertex_num; ++ i){
			a = bidirected_vertex[(i << 1)];
			b = bidirected_vertex[(i << 1) + 1];
			undirected_edges[a].insert(b);
			undirected_edges[b].insert(a);
		}
		for (i = 0; i < directed_vertex_num; ++ i){
			a = directed_vertex_in[i];
			b = directed_vertex_out[i];
			undirected_edges[a].insert(b);
			undirected_edges[b].insert(a);
		}
	}
	
	edge_offset[0] = 0;
	E_Sum = 0;
	for (i = 1; i <= nV; ++ i){
		edge_offset[i] = edge_offset[i - 1] + undirected_edges[i - 1].size();
		E_Sum += undirected_edges[i].size();
		//fprintf(stderr, "%d ", undirected_edges[i].size());
		for (j = 0, pSet = undirected_edges[i].begin(); j < (int)undirected_edges[i].size(); ++ j, ++ pSet){
			edges[edge_offset[i] + j] = *pSet;
		}
	}
	//puts("");
	edge_offset[nV + 1] = E_Sum;
	//fprintf(stderr, "random ends, num of edges is %d\n", E_Sum);
	
}
