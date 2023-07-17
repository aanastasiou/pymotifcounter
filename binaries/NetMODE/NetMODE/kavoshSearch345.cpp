#include"common.h"
using namespace std;

void* kavoshSearch345(void *darg)
{
	args_t *arg = (args_t *) darg;
	int &subgraph_size   = arg->subgraph_size;
	int &graph_size      = arg->graph_size;
	int &row_size        = arg->row_size;
	int *&adj_mat        = arg->adj_mat; 

	int root, remain, depth, isNewCall;
	int vis_left[10], cho_left[10]; 
	int mStack[10], choosen[10];
	int *visList, *visited;

	visited = new int[(graph_size >> 5) + 1];
	visList = new int[graph_size + 1];
	int t = (graph_size >> 5) + 1;
	int m, findNext;
	int v, tv, x;
	int i, j, k;

	for (i = 0; i < t; ++ i){
		visited[i] = 0;
	}
	for (root = 1; root <= graph_size; ++ root){
		//printf("root = %d\n", root);
		visList[0] = root;
		visited[root >> 5] |= (1 << (root & 31));
		vis_left[0] = cho_left[0] = 0;
		vis_left[1] = cho_left[1] = 1;
		remain = subgraph_size - 1;
		choosen[0] = 0;

		depth = 1;
		isNewCall = 1;
		x = 0;
		do{
			if (isNewCall){
				++ depth;
				if (remain == 0){
					++ arg->origin_subgraph_count[ arg->pattern[x] ];
					isNewCall = 0;
				} else{ // remain != 0

					for (i = cho_left[depth - 2], k = vis_left[depth - 1]; i < cho_left[depth - 1]; ++ i){
						v = visList[choosen[i]];
						for (j = arg->edge_offset[v]; j < arg->edge_offset[v + 1]; ++ j){ //iterate over the edge 
							tv = arg->edges[j];
							if ( tv > root && !(visited[tv >> 5] & (1 << (tv & 31))) ){
								visited[tv >> 5] |= (1 << (tv & 31));
								visList[k] = tv;
								++ k;
							}
						}
					}
					vis_left[depth] = k;
					if (vis_left[depth] - vis_left[depth - 1] > 0){
						cho_left[depth] = cho_left[depth - 1] + 1;
						choosen[cho_left[depth - 1]] = vis_left[depth - 1];

						k = cho_left[depth - 1];
						v = visList[choosen[k]];
						++ k;
						for (j = 1; j < k; ++ j){
							tv = visList[choosen[j - 1]];
							if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
								x |= (1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j));
							}
							else{
								x &= (~(1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j)));
							}
							if (((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31)))) != 0){
								x |= (1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k));
							}
							else{
								x &= (~(1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k)));
							}
						} 


						-- remain;
						isNewCall = 1;
						mStack[depth] = 1;


					} else{
						mStack[depth] = subgraph_size;
						isNewCall = 0;
					}
				}
			} else{ // ! isNewCall
				-- depth;

				m = mStack[depth];
				remain += m;
				i = 1;
				findNext = 0;

				while (!findNext){
					if (m > vis_left[depth] - vis_left[depth - 1] || m > remain) break;
					while ( (choosen[cho_left[depth] - i] + i >= vis_left[depth]) && (i <= m) ){
						++ i;
					}

					if (i > m){
						++ m;
						if (m > vis_left[depth] - vis_left[depth - 1] || m > remain) break;
						cho_left[depth] = cho_left[depth - 1] + m;
						for (i = 0; i < m; ++ i){
							choosen[cho_left[depth - 1] + i] = vis_left[depth - 1] + i;

							k = cho_left[depth - 1] + i;
							v = visList[choosen[k]];
							++ k;
							for (j = 1; j < k; ++ j){
								tv = visList[choosen[j - 1]];
								if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
									x |= (1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j));
								}
								else{
									x &= (~(1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j)));
								}
								if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
									x |= (1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k));
								}
								else{
									x &= (~(1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k)));
								}
							}

						}
						i = 1;
						-- choosen[cho_left[depth] - i];
						continue;
					}
					else{
						++ choosen[cho_left[depth] - i];

						k = cho_left[depth] - i;
						v = visList[choosen[k]];
						++ k;
						for (j = 1; j < k; ++ j){
							tv = visList[choosen[j - 1]];
							if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
								x |= (1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j));
							}
							else{
								x &= (~(1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j)));
							}
							if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
								x |= (1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k));
							}
							else{
								x &= (~(1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k)));
							}
						}

						while (-- i, i > 0){
							choosen[cho_left[depth] - i] = choosen[cho_left[depth] - i - 1] + 1;

							k = cho_left[depth] - i;
							v = visList[choosen[k]];
							++ k;
							for (j = 1; j < k; ++ j){
								tv = visList[choosen[j - 1]];
								if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
									x |= (1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j));
								}
								else{
									x &= (~(1 << ((subgraph_size - k) * subgraph_size + subgraph_size - j)));
								}
								if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
									x |= (1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k));
								}
								else{
									x &= (~(1 << ((subgraph_size - j) * subgraph_size + subgraph_size - k)));
								}
							}
						}
						findNext = 1;
					}
				}

				if (!findNext){
					isNewCall = 0;
					for (i = vis_left[depth - 1]; i < vis_left[depth]; ++ i){
						tv = visList[i];
						visited[tv >> 5] &= (~(1 << (tv & 31)));
					}
				}
				else{
					mStack[depth] = m;
					isNewCall = 1;
					remain -= m;
				}
			}
		}while ((depth > 2) || (isNewCall == 1));
	} // end of for(root)
	
	delete[] visited;
	delete[] visList;

	return NULL;
}

