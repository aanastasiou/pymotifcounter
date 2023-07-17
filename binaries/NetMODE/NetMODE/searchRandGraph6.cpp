#include "common.h"
using namespace std;
#define hash_macro(x,RT) x = 1;\
						for (i = 0;i < 6;i++){\
							x = x * 3 * RT.elem[i] + RT.elem[i];\
							if (i > 0) {\
								x -= (RT.elem[i]) ^ RT.elem[i-1];\
							}\
						}\
						x = abs(x);\
						x %= MAXHASHSIZE;
						
void *searchRandGraph6(void *darg)
{
	args_t *arg				= (args_t*) darg;

	Tup6_t *subgraph_ref	= arg->subgraph_ref;
	HashLink_t *hash_table	= arg->hash_table;
	ULL*exception_table		= arg->exception_table;
	int subgraph_size		= arg->subgraph_size;
	int graph_size			= arg->graph_size;
	int row_size			= arg->row_size;
	int *edges				= arg->edges;
	int *edge_offset		= arg->edge_offset;
	int *adj_mat			= arg->adj_mat;
	ULL *this_subgraph_count= arg->this_subgraph_count;
	int *exception_id		= arg->exception_id;

/*
 *    arg->pr();
 *
 *    printf("offset = ");
 *    for (int j = 0;j < graph_size + 1;j++) {
 *        printf("%d ", edge_offset[j]);
 *    }
 *    putchar(10);
 *
 *    printf("edges = ");
 *    for (int j = 0;j < edge_offset[graph_size + 1];j++) {
 *        printf("%d ", edges[j]);
 *    }
 *    putchar(10);
 */

	int root, remain, depth, isNewCall;
	int list_left[10], choo_left[10];
	// list_left is right bound of visList
	// choo_left is right bound of choonsen list
	bool GraphMat[10][10];
	int PreX[6][6][6];
	int mStack[10], choosen[10];
	int *visList, *visited;
	Tup6_t T, RT;
	HashLink_t pHT;

	ULL sg6 = 0, sg1 = 1;

	visited = new int[(graph_size >> 5) + 1];
	visList = new int[graph_size + 3];
	int t = (graph_size >> 5) + 1;
	int m, findNext;
	int v, tv, x, y;
	int i, j, k, ti, tj, tk;

	for (i = 0;i <= graph_size;i++) { visList[i] = 0; }
	for (i = 0; i < t; ++ i){ visited[i] = 0; } 
	for (i = 0; i < 6; ++ i){ T.elem[i] = 0; }

	for (k = 0; k < 6; ++ k){
		for (j = 0; j < k; ++ j){
			for (i = 0; i < 6; ++ i){
				if (i == j || i == k){
					PreX[i][j][k] = -1;
					continue;
				}
				if (i < k) tk = k - 1; else tk = k;
				if (i < j) tj = j - 1; else tj = j;
				PreX[i][k][j] = tk * 5 + tj;
				PreX[i][j][k] = tj * 5 + tk;
			}
		}
	}

	for (root = 1; root <= graph_size; ++ root){
		//printf("root = %d\n", root);
		visList[0] = root;
		visited[root >> 5] |= (1 << (root & 31));
		list_left[0] = choo_left[0] = 0;
		list_left[1] = choo_left[1] = 1;
		remain = subgraph_size - 1;
		choosen[0] = 0;

		depth = 1;
		isNewCall = 1;
		x = 0;
		do{
			if (isNewCall){
				++ depth;
				if (remain == 0){
					// check sg6 for exception
					ULL hCode = sg6 % EXCMOD;
					if (exception_table[hCode] == sg6){
						++ this_subgraph_count[exception_id[hCode]];
					}
					else{
						for (k = 0; k < 6; ++ k){
							RT.elem[k] = arg->pattern[T.elem[k]];
						}
						sort(RT.elem, RT.elem + 6);
						//* get hash code
						hash_macro(x, RT);
						//  hash code got */

						//* check hash table
						pHT = hash_table[x];
						y = 0;
						while (pHT != 0){
							j =  pHT ->num;
							y = 1;
							for (i = 0; i < 6; ++ i){
								if (RT.elem[i] != subgraph_ref[j].elem[i]){
									y = 0;
									break;
								}
							}
							if (y){
								break;
							}
							else{
								pHT = pHT->next;
							}
						}
						// check end */

						if (y){
							i = pHT ->num;
							++ this_subgraph_count[i];
						}
					}
					isNewCall = 0;
				}
				else{

					for (i = choo_left[depth - 2], k = list_left[depth - 1]; i < choo_left[depth - 1]; ++ i){
						v = visList[choosen[i]];
						for (j = edge_offset[v]; j < edge_offset[v + 1]; ++ j) {
							tv = edges[j];
/*
 *                            if (tv > graph_size) {
 *                                printf("isNewCall = %d\n", isNewCall);
 *                                printf("depth = %d\n", depth);
 *                                for (int i = 0;i < 10;i++) { printf("choo_left[%d] = %d\n", i, choo_left[i]); }
 *                                for (int i = 0;i < 10;i++) { printf("list_left[%d] = %d\n", i, list_left[i]); }
 *                                for (int i = 0;i < 10;i++) { printf("choosen[%d] = %d\n", i, choosen[i]); }
 *
 *                                printf("i = %d, choosen[i] = %d, visList[choosen[i] = %d, v = %d, tv = %d\n", 
 *                                        i, choosen[i], visList[choosen[i]], v, tv);
 *                                printf("%d , %d\n", edge_offset[v], edge_offset[v+1]);
 *                                for (int i = 0;i < edge_offset[graph_size+1];i++) {
 *                                    printf("%d ", edges[i]);
 *                                }
 *                                putchar(10);
 *                                exit(0);
 *                            }
 */

							if ( tv > root && !(visited[tv >> 5] & (1 << (tv & 31))) ){
								visited[tv >> 5] |= (1 << (tv & 31));
								visList[k] = tv;
								++ k;
							}
						}
					}
					list_left[depth] = k;
					if (list_left[depth] - list_left[depth - 1] > 0){
						choo_left[depth] = choo_left[depth - 1] + 1;
						choosen[choo_left[depth - 1]] = list_left[depth - 1];

						//* add to SubGraph
						k = choo_left[depth - 1];
						v = visList[choosen[k]];
						for (j = 0; j < k; ++ j){
							tv = visList[choosen[j]];
							//GraphMat[k][j] = ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0);
							if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] |= (1 << PreX[ti][k][j]);
								}
								sg6 |= (sg1 << (k * 6 + j));
							}
							else{
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] &= (~(1 << PreX[ti][k][j]));
								}
								sg6 &= (~(sg1 << (k * 6 + j)));
							}
							//GraphMat[j][k] = ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0);
							if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] |= (1 << PreX[ti][j][k]);

								}
								sg6 |= (sg1 << (j * 6 + k));
							}
							else{
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] &= (~(1 << PreX[ti][j][k]));
								}
								sg6 &= (~(sg1 << (j * 6 + k)));
							}
						} 
						GraphMat[k][k] = 0;
						// add end */

						-- remain;
						isNewCall = 1;
						mStack[depth] = 1;
					}
					else{
						mStack[depth] = subgraph_size;
						isNewCall = 0;
					}
				}
			}
			else{
				-- depth;

				m = mStack[depth];
				remain += m;
				i = 1;
				findNext = 0;

				while (!findNext){
					if (m > list_left[depth] - list_left[depth - 1] || m > remain) break;
					while ( (choosen[choo_left[depth] - i] + i >= list_left[depth]) && (i <= m) ){
						++ i;
					}
					if (i > m){
						++ m;
						if (m > list_left[depth] - list_left[depth - 1] || m > remain) break;
						choo_left[depth] = choo_left[depth - 1] + m;
						for (i = 0; i < m; ++ i){
							choosen[choo_left[depth - 1] + i] = list_left[depth - 1] + i;

							//* add to SubGraph
							k = choo_left[depth - 1] + i;
							v = visList[choosen[k]];
							for (j = 0; j < k; ++ j){
								tv = visList[choosen[j]];
								//GraphMat[k][j] = ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0);
								if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] |= (1 << PreX[ti][k][j]);
									}
									sg6 |= (sg1 << (k * 6 + j));
								}
								else{
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] &= (~(1 << PreX[ti][k][j]));
									}
									sg6 &= (~(sg1 << (k * 6 + j)));
								}
								//GraphMat[j][k] = ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0);
								if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] |= (1 << PreX[ti][j][k]);

									}
									sg6 |= (sg1 << (j * 6 + k));
								}
								else{
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] &= (~(1 << PreX[ti][j][k]));
									}
									sg6 &= (~(sg1 << (j * 6 + k)));
								}
							}
							GraphMat[k][k] = 0;
							// add end */

						}
						i = 1;
						-- choosen[choo_left[depth] - i];
						continue;
					}
					else{
						++ choosen[choo_left[depth] - i];
						//* add to SubGraph
						k = choo_left[depth] - i;
						v = visList[choosen[k]];
						for (j = 0; j < k; ++ j){
							tv = visList[choosen[j]];
							//GraphMat[k][j] = ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0);
							if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] |= (1 << PreX[ti][k][j]);
								}
								sg6 |= (sg1 << (k * 6 + j));
							}
							else{
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] &= (~(1 << PreX[ti][k][j]));
								}
								sg6 &= (~(sg1 << (k * 6 + j)));
							}
							//GraphMat[j][k] = ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0);
							if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] |= (1 << PreX[ti][j][k]);

								}
								sg6 |= (sg1 << (j * 6 + k));
							}
							else{
								for (ti = 0; ti < 6; ++ ti){
									if (ti == k || ti == j) continue;
									T.elem[ti] &= (~(1 << PreX[ti][j][k]));
								}
								sg6 &= (~(sg1 << (j * 6 + k)));
							}
						}
						GraphMat[k][k] = 0;
						// add end */
						while (-- i, i > 0){
							choosen[choo_left[depth] - i] = choosen[choo_left[depth] - i - 1] + 1;
							//* add to SubGraph
							k = choo_left[depth] - i;
							v = visList[choosen[k]];
							for (j = 0; j < k; ++ j){
								tv = visList[choosen[j]];
								//GraphMat[k][j] = ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0);
								if ((adj_mat[v * row_size + (tv >> 5)] & (1 << (tv & 31))) != 0){
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] |= (1 << PreX[ti][k][j]);
									}
									sg6 |= (sg1 << (k * 6 + j));
								}
								else{
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] &= (~(1 << PreX[ti][k][j]));
									}
									sg6 &= (~(sg1 << (k * 6 + j)));
								}
								//GraphMat[j][k] = ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0);
								if ((adj_mat[tv * row_size + (v >> 5)] & (1 << (v & 31))) != 0){
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] |= (1 << PreX[ti][j][k]);

									}
									sg6 |= (sg1 << (j * 6 + k));
								}
								else{
									for (ti = 0; ti < 6; ++ ti){
										if (ti == k || ti == j) continue;
										T.elem[ti] &= (~(1 << PreX[ti][j][k]));
									}
									sg6 &= (~(sg1 << (j * 6 + k)));
								}
							}
							GraphMat[k][k] = 0;
							// add end */
						}
						findNext = 1;
					}
				}

				if (!findNext){
					isNewCall = 0;
					for (i = list_left[depth - 1]; i < list_left[depth]; ++ i){
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
	
	double count_sum = 0;
	if(verbose) { 
		string str="";
		for (int i = 1;i <= arg->pattern_num; ++ i) {
			if (arg->origin_subgraph_count[i] == 0) continue;
			str += convertULLtoString(arg->this_subgraph_count[i]); str += " ";
			count_sum += arg->this_subgraph_count[i];
			arg->subgraph_count[i]   += arg->this_subgraph_count[i];
			arg->subgraph_count_2[i] += SQR(arg->this_subgraph_count[i]);
		}
		str+=";\n"; cout << str;
	}
	else {
		for (int i = 1;i <= arg->pattern_num; ++ i) {
			count_sum += this_subgraph_count[i];
			arg->subgraph_count[i]   += this_subgraph_count[i];
			arg->subgraph_count_2[i] += SQR(this_subgraph_count[i]);	
		}
		for (int i = 1; i <= arg->pattern_num; ++ i){
			arg->subgraph_concentration[i]   += this_subgraph_count[i] / count_sum;
			arg->subgraph_concentration_2[i] += SQR(this_subgraph_count[i] / count_sum);
		}
		for (int i = 1; i <= arg->pattern_num; ++ i){
			if (arg->this_subgraph_count[i] >= arg->origin_subgraph_count[i]){
				++ arg->subgraph_p_value[i];
			}
			if (arg->this_subgraph_count[i] / count_sum >= arg->origin_subgraph_count[i] / arg->origin_subgraph_sum){
				++ arg->subgraph_cp_value[i];
			}
		}
	}
	arg->vacancy[arg->vacancy_num] = true;
	return NULL;
}

