
#ifndef ThreadManager_h
#define ThreadManager_h

#include <pthread.h>
#include <cassert>
#include <queue>
#include <unistd.h>
using namespace std;

struct Job 
{
	void *(*task)(void*);
	void *arg;
	Job(void *(*t)(void*), void *a);
};

class ThreadManager
{
	public:
		int running, running_jobs, thread_num;
		ThreadManager (int size);
		~ThreadManager ();
		pthread_mutex_t mutex0, mutex1, mutex2;
		pthread_t *threads;
		queue<Job> jobs;

		void worker();

		int append(void *(*task)(void*), void *real); 
		int size();
		/* append the Job to the queue*/

		void sync();
};

#endif //ThreadManager_h
