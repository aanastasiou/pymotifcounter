/* Every problem has a simple, fast and wrong solution */
#include "common.h"
#include "TM.h"
#include "time.h" /* needed to compile under cygwin */

#define _TEST
//#define _DEBUG

using namespace std; 

Tup6_t *subgraph_ref;
HashLink_t hash_table[MAXHASHSIZE]; 

int exception_id[EXCMOD + 1];
ULL exception_table[EXCMOD + 1];

vector <ULL> real_adj;

void die()
{
	fputs("-k --size    = k-node subgraphs (=3,4,5 or 6)\n", stderr);
	fputs("-c --random  = # comparison graphs (some number, could be 0, an integer in [0, 2^31))\n", stderr);
	fputs("-b --burnin  = burnin = # comparison graphs discarded (some number, could be 0)\n", stderr);
	fputs("-e --method  = bidirectional edge random_method (=0, 1, 2, 3(default) or 4)\n               0: fixed;\n               1: no regard;\n               2: global constant;\n               3: local constant;\n               4: uniform.\n", stderr);
	fputs("-t --thread  = number of threads to run\n", stderr);
	fputs("-v --verbose = interface mode (for interfacing with e.g. R) (=0 (default), 1)\n", stderr);
	fputs("-s --showall = show all subgraph statistics in random network while (k <= 5)\n", stderr);
	exit(1);
}

void dieChk(bool condition, string s)
{
	if (false == condition) {
		fprintf(stderr, "%s\n", s.c_str());
		die();
	}
}

void printEdges(int edges[], int n)
{
	for (int i = 0;i < n;i++) {
		printf("edges[%d] = %d\n", i, edges[i]);
	}
	putchar(10);
}



void printAdjMat(ULL stat, int subgraph_size, FILE *fout)
{
        string str;
	fprintf(fout,"graphID = %llu\n",stat);
	for (int i = 0;i < subgraph_size;i++) {
		for (int j = 0;j < subgraph_size;j++) {
			str = convertULLtoString(stat & 1) + str;
			stat >>= 1;
		}
		str = "\n" + str;
	}
	str += "\n\n\n";
	fprintf(fout,"%s",str.c_str());
}



int pattern[(1 << 25) + 10]; 

class Motif 
{
	public:

		int NumOfExchange;
		int random_graph_num;

		int pattern_num; 

		ULL origin_subgraph_sum;
		ULL random_subgraph_sum; 

		int THREAD_NUM; 
		ULL burnin;
		int random_method;


		int *pattern_map;

		args_t *args;

		args_t opt[1];
		ThreadManager *thread_manager;
		
		bool *vacancy;


		void parseArgs(int argc, char *argv[])
		{

			if (argc == 1) { die(); }
			//if ((argc - 1) % 2 != 0) { die(); }
			for (int i = 1;i < argc;i += 1) {
				string cmd = string(argv[i]);
				if (cmd == "-k" || cmd == "--size") { if (1 != sscanf(argv[++i], "%d", &opt->subgraph_size)) { die(); }
				}else if (cmd == "-c" || cmd == "--random") { if (1 != sscanf(argv[++i], "%d", &random_graph_num)) { die(); }
				}else if (cmd == "-b" || cmd == "--burnin") { if (1 != sscanf(argv[++i], "%llu", &burnin)) { die(); }
				}else if (cmd == "-e" || cmd == "--method") { if (1 != sscanf(argv[++i], "%d", &random_method)) { die(); }
				}else if (cmd == "-v" || cmd == "--verbose") { if (1 != sscanf(argv[++i], "%d", &verbose)) { die(); }
				}else if (cmd == "-t" || cmd == "--thread") { if (1 != sscanf(argv[++i], "%d", &THREAD_NUM)) { die(); }
				}else if (cmd == "-s" || cmd == "--showall") { showall = 1;
				}else {
					die();
				}
			}

			dieChk(3 <= opt->subgraph_size && opt->subgraph_size <= 6, "subgraph_size should (3, 4, 5, 6)");
			dieChk(random_graph_num >= 0, "random_graph_num should >= 0");
			dieChk(burnin >= 0, "burnin should >= 0");
			dieChk(random_method >= 0 && random_method <= 4, "random_method should be (0, 1, 2, 3)");
			dieChk(THREAD_NUM >= 1, "thread_num should >= 1");
			random_method = 1 << random_method;
			
			if (opt->subgraph_size > 5) showall = 0;
			
			if (readData(opt) != 0) {
				die();
			}
		}

		Motif(int argc, char *argv[]):	
			NumOfExchange (3),
			random_graph_num (0),
			pattern_num (0),
			origin_subgraph_sum (0),
			random_subgraph_sum (0),
			THREAD_NUM(1),
			burnin(0),
			random_method(3)
	{
		parseArgs(argc, argv);

		srand(time(0));
		//srand(11);

		if (opt->subgraph_size < 6) {
			generateSubgraph(pattern, pattern_map, opt->subgraph_size, pattern_num);

		}else {
			generateSubgraph(pattern, pattern_map, 5, pattern_num);
			handleExceptions(exception_id, exception_table);
		}

		opt->pattern         = pattern;
		opt->subgraph_ref    = subgraph_ref;
		opt->hash_table      = hash_table;
		opt->exception_id    = exception_id;
		opt->exception_table = exception_table; 

		if (opt->subgraph_size < 6) {
			opt->pattern_num		 = pattern_num;
			opt->origin_subgraph_count.resize(pattern_num + 1);

			opt->subgraph_count      = new ULL[pattern_num + 1];
			opt->subgraph_count_2    = new ULL[pattern_num + 1];
			opt->this_subgraph_count = new ULL[pattern_num + 1]; 
			
			opt->subgraph_p_value    = new int[pattern_num + 1];
			opt->subgraph_cp_value    = new int[pattern_num + 1];
			
			opt->subgraph_concentration   = new double[pattern_num + 1];
			opt->subgraph_concentration_2 = new double[pattern_num + 1];

			memset(opt->subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
			memset(opt->subgraph_count_2, 0, sizeof(ULL) * (pattern_num + 1));
			memset(opt->this_subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
			
			memset(opt->subgraph_p_value, 0, sizeof(int) * (pattern_num + 1));
			memset(opt->subgraph_cp_value, 0, sizeof(int) * (pattern_num + 1));
			
			memset(opt->subgraph_concentration, 0, sizeof(double) * (pattern_num + 1));
			memset(opt->subgraph_concentration_2, 0, sizeof(double) * (pattern_num + 1));

			kavoshSearch345(opt);
		}else {
			/* origin_subgraph_count is resized in kavoshSearch6. */
			kavoshSearch6(opt);
			subgraph_ref = opt->subgraph_ref;
			
			opt->pattern_num = opt->origin_subgraph_count[0]; 
			pattern_num      = opt->origin_subgraph_count[0]; 

			opt->subgraph_count      = new ULL[pattern_num + 1];
			opt->subgraph_count_2    = new ULL[pattern_num + 1];
			opt->this_subgraph_count = new ULL[pattern_num + 1];
			
			opt->subgraph_p_value    = new int[pattern_num + 1];
			opt->subgraph_cp_value    = new int[pattern_num + 1];
			
			opt->subgraph_concentration   = new double[pattern_num + 1];
			opt->subgraph_concentration_2 = new double[pattern_num + 1];

			memset(opt->subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
			memset(opt->subgraph_count_2, 0, sizeof(ULL) * (pattern_num + 1));
			memset(opt->this_subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
			
			memset(opt->subgraph_p_value, 0, sizeof(int) * (pattern_num + 1));
			memset(opt->subgraph_cp_value, 0, sizeof(int) * (pattern_num + 1));
			
			memset(opt->subgraph_concentration, 0, sizeof(double) * (pattern_num + 1));
			memset(opt->subgraph_concentration_2, 0, sizeof(double) * (pattern_num + 1));
		}
		
		origin_subgraph_sum = 0;
		for (int i = 1;i <= pattern_num;i++) {
			origin_subgraph_sum += opt->origin_subgraph_count[i];
		}
		
		opt->origin_subgraph_sum = origin_subgraph_sum;

		if(verbose) {
		  int non_zero_count=0;
		  for (int z = 1;z < pattern_num;z++) {
		    if (opt->origin_subgraph_count[z] != 0) non_zero_count++;
		  }
		  printf("%d ;\n",non_zero_count);
		  for (int z = 1;z < pattern_num;z++) {
		    if (opt->origin_subgraph_count[z] == 0) continue;
		    if(opt->subgraph_size < 6) { printf("%d ",pattern_map[z]); } else { printf("%llu ",real_adj[z]); } 
		  }
		  printf(";\n");
		  for (int z = 1;z < pattern_num;z++) {
		    if (opt->origin_subgraph_count[z] == 0) continue;
		    printf("%llu ",opt->origin_subgraph_count[z]);
		  }
		  printf(";\n");
		}

	} 


		void run()
		{
			thread_manager       = new ThreadManager(THREAD_NUM); 
			args                 = new args_t[THREAD_NUM];
			vacancy	             = new bool[THREAD_NUM];
			
			for (int i = 0; i < THREAD_NUM; ++ i){
				vacancy[i] = true;
			}
			
			for (int i = 0; i < THREAD_NUM; ++ i) {
				int edges_size = opt->sizeof_edges;
				int adj_size   = opt->row_size * (opt->graph_size + 1) + 3;

				args[i]                     = *opt;
				args[i].edges               = new int[edges_size];
				args[i].edge_offset         = new int[opt->graph_size + 3];
				args[i].adj_mat             = new int[adj_size]; 

				args[i].subgraph_count      = new ULL[pattern_num + 1];
				args[i].subgraph_count_2    = new ULL[pattern_num + 1];
				args[i].this_subgraph_count = new ULL[pattern_num + 1];
				
				args[i].subgraph_p_value    = new int[pattern_num + 1];
				args[i].subgraph_cp_value    = new int[pattern_num + 1];
				
				args[i].subgraph_concentration  = new double[pattern_num + 1];
				args[i].subgraph_concentration_2 = new double[pattern_num + 1];

				memset(args[i].subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
				memset(args[i].subgraph_count_2, 0, sizeof(ULL) * (pattern_num + 1));
				memset(args[i].this_subgraph_count, 0, sizeof(ULL) * (pattern_num + 1));
				
				memset(args[i].subgraph_p_value, 0, sizeof(int) * (pattern_num + 1));
				memset(args[i].subgraph_cp_value, 0, sizeof(int) * (pattern_num + 1));
				
				memset(args[i].subgraph_concentration, 0, sizeof(double) * (pattern_num + 1));
				memset(args[i].subgraph_concentration_2, 0, sizeof(double) * (pattern_num + 1));
				
				args[i].vacancy = vacancy;
			}

			for (ULL i = 1, steps = (burnin / 10); i <= burnin; ++ i) {
				genRandomGraph(opt->graph_size, opt->row_size, NumOfExchange, opt->edges, opt->edge_offset, opt->adj_mat, random_method);
				if (!verbose){
					if ((-- steps) == 0){
						fprintf(stderr, "burnin process %llu, %.0lf%%\n", i, (double(i)) / burnin * 100);
						steps = burnin / 10;
					}
				}
			}

			//clock_t start = clock();
			
			#ifndef _TEST
				int steps = (random_graph_num / 10);
			#endif
			for (int i = 0; i < random_graph_num; ++ i) {
				#ifdef _DEBUG
					printf("%d\n", i);
				#endif
				
				genRandomGraph(opt->graph_size, opt->row_size, NumOfExchange, opt->edges, opt->edge_offset, opt->adj_mat, random_method); 
				
				while (thread_manager->size() >= THREAD_NUM) {
					usleep(10);
				}
				
				#ifndef _TEST
				if (!verbose){
					if ((-- steps) == 0){
						fprintf(stderr, "random graph process %d, %.0lf%%\n", i + 1, (double(i + 1)) / random_graph_num * 100);
						steps = random_graph_num / 10;
					}
				}
				#endif
				//fprintf(stderr, "going to process %d of %d random graphs", i + 1, random_graph_num);
				/*if (i > THREAD_NUM && i % THREAD_NUM == 0) {
					clock_t current = clock();
					double cost = 1.0 * (current - start) / CLOCKS_PER_SEC / 3600.0;
					double time_left =  cost * (random_graph_num - i + 1)/ THREAD_NUM / i;
					fprintf(stderr, ", estimate [cost:%.6f, left:%.3f] hours", 1.0 * cost , time_left);
				}*/
				//fprintf(stderr, "\n");
				
				args_t *self = NULL;
				
				for (int j = 0; j < THREAD_NUM; ++ j){
					if (vacancy[j]){
						vacancy[j] = false;
						self = &args[j]; 
						self->vacancy_num = j;
						break;
					}
				}
				for (int j = 0;j < opt->edge_offset[opt->graph_size + 1];j++) {
					self->edges[j] = opt->edges[j];
				}
				for (int j = 0;j < opt->graph_size + 3;j++) {
					self->edge_offset[j] = opt->edge_offset[j];
				}
				for (int j = 0;j < opt->row_size * (opt->graph_size + 1) + 1;j++) {
					self->adj_mat[j] = opt->adj_mat[j];
				}

				fill(self->this_subgraph_count, self->this_subgraph_count + pattern_num + 1, 0);

				//args[self].pr();

				if (opt->subgraph_size < 6) {
					thread_manager->append(searchRandGraph345, self);
				}else {
					thread_manager->append(searchRandGraph6  , self);
				}
			}
		}

		void fin()
			/* reduction and do statistics */
		{
			//printf("finish work\n");
			
			thread_manager->sync(); 
			
			//printf("start calc\n");
			
			//printf("calc sum\n");
			
			//printf("\nTotal Number of Original subgraph_count: %llu\n", origin_subgraph_sum);
			for (int i = 0; i < THREAD_NUM; ++ i) {
				for (int j = 1; j <= pattern_num; ++ j) {
					args_t &self = args[i];
					random_subgraph_sum      += self.subgraph_count[j];
					opt->subgraph_count[j]   += self.subgraph_count[j];
					opt->subgraph_count_2[j] += self.subgraph_count_2[j];
					
					opt->subgraph_p_value[j] += self.subgraph_p_value[j];
					opt->subgraph_cp_value[j] += self.subgraph_cp_value[j];
					
					opt->subgraph_concentration[j]   += self.subgraph_concentration[j];
					opt->subgraph_concentration_2[j] += self.subgraph_concentration_2[j];
				}
			}
			
			
			if (!verbose) {
				/// output
				
				printf("calc Z-Score\n");
				
				for (int i = 1; i <= pattern_num; ++ i) {
					if (pattern_map[i] == 0) continue;
					if (showall){
						if (opt->origin_subgraph_count[i] == 0 && opt->subgraph_concentration[i] == 0) continue;
					}else{
						if (opt->origin_subgraph_count[i] == 0) continue;
					}					
					
					double X    = 1.0 * opt->origin_subgraph_count[i];
					double EX   = 1.0 * opt->subgraph_count[i] / random_graph_num;
					double EX2  = 1.0 * opt->subgraph_count_2[i] / random_graph_num;
					double SD   = 1.0 * sqrt(EX2 - EX * EX);
					double ZScore = (X - EX) / SD;

					double cX    = 1.0 * opt->origin_subgraph_count[i] / origin_subgraph_sum;
					double cEX   = 1.0 * opt->subgraph_concentration[i] / random_graph_num;
					double cEX2  = 1.0 * opt->subgraph_concentration_2[i] / random_graph_num;
					double cSD   = 1.0 * sqrt(cEX2 - cEX * cEX);
					double cZScore = (cX - cEX) / cSD;

					double pValue = opt->subgraph_p_value[i] * 1.0 / random_graph_num;
					double cpValue = opt->subgraph_cp_value[i] * 1.0 / random_graph_num; 

					if (opt->subgraph_size == 3) { printf("gID: %3d  freq: %5llu  ave_rand_freq: %8.2f (sd: %6.3f)  conc: %.5f  ave_rand_conc: %.5f (sd: %.7f)  f-ZScore: %6.2f  f-pValue: %.8lf  c-ZScore: %6.2f  c-pValue: %.8lf\n",pattern_map[i], opt->origin_subgraph_count[i], EX, SD, cX, cEX, cSD, ZScore, pValue, cZScore, cpValue); }
					else if (opt->subgraph_size == 4) { printf("gID: %5d  freq: %5llu  ave_rand_freq: %8.2f (sd: %7.3f)  conc: %.5f  ave_rand_conc: %.5f (sd: %.7f)  f-ZScore: %7.2f  f-pValue: %.8lf  c-ZScore: %7.2f  c-pValue: %.8lf\n",pattern_map[i], opt->origin_subgraph_count[i], EX, SD, cX, cEX, cSD, ZScore, pValue, cZScore, cpValue); }
					else if (opt->subgraph_size == 5) { printf("gID: %8d  freq: %6llu  ave_rand_freq: %9.2f (sd: %8.3f)  conc: %.6f  ave_rand_conc: %.6f (sd: %.8f)  f-ZScore: %7.2f  f-pValue: %.8lf  c-ZScore: %7.2f  c-pValue: %.8lf\n",pattern_map[i], opt->origin_subgraph_count[i], EX, SD, cX, cEX, cSD, ZScore, pValue, cZScore, cpValue); }
					else { printf("gID: %11llu  freq: %7llu  ave_rand_freq: %10.2f (sd: %9.3f)  conc: %.7f  ave_rand_conc: %.7f (sd: %.9f)  f-ZScore: %7.2f  f-pValue: %.8lf  c-ZScore: %7.2f  c-pValue: %.8lf\n",real_adj[i], opt->origin_subgraph_count[i], EX, SD, cX, cEX, cSD, ZScore, pValue, cZScore, cpValue); }
				}
				
				//printf("output adjmat\n");
				
				FILE *fout = fopen("adjMat.txt", "w");
				if (opt->subgraph_size == 6) { fprintf(fout,"Warning: graphIDs are not necessarily canonical.\n\n\n"); }
				for (int i = 1;i <= pattern_num;i++) {
					if (opt->origin_subgraph_count[i] == 0) continue; 
					if (opt->subgraph_size < 6) {
						printAdjMat(pattern_map[i], opt->subgraph_size, fout);
					}else {
						printAdjMat(real_adj[i],    opt->subgraph_size, fout);
					}
				}
				fclose(fout);
			}
		}

		~Motif()
		{
			/*
			delete thread_manager; 

			delete []opt->edges;
			delete []opt->edge_offset; 
			delete []opt->adj_mat;
			delete []opt->subgraph_count; 
			delete []opt->subgraph_count_2; 
			delete []opt->this_subgraph_count; 

			for (int i = 0;i < THREAD_NUM;i++) {
				args_t *self = &args[i];
				delete []self->edges;
				delete []self->edge_offset; 
				delete []self->adj_mat;
				delete []self->subgraph_count; 
				delete []self->subgraph_count_2; 
				delete []self->this_subgraph_count; 
			}

			delete [] args;
			*/
		}

}; 

int main(int argc, char *argv[])
{
	Motif motif(argc, argv);
	motif.run();
	motif.fin();
	return 0;
}

