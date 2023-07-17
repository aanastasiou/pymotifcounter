#include "TM.h"
#include "common.h"
using namespace std;

/* delcare static member in other ThreadManager.h */
//pthread_mutex_t ThreadManager::mutex0, ThreadManager::mutex1;
//int ThreadManager::running;

void* wrapper(void* param)
{
     ThreadManager* t = (ThreadManager*)param;
     t->worker();
    return NULL;
}

Job::Job(void *(*t)(void*) = NULL, void *a = NULL):task(t), arg(a) {}

ThreadManager::ThreadManager (int size) {
	running = true; 
	running_jobs = 0;
	thread_num = size;

	pthread_mutex_init(&mutex0, NULL);
	pthread_mutex_init(&mutex1, NULL);
	pthread_mutex_init(&mutex2, NULL);

	threads = new pthread_t[size];
	for (int i = 0;i < size;i++) {
		int rc = pthread_create(&threads[i], NULL, wrapper, (void*)this);
		assert(rc == 0);
	}
}

ThreadManager::~ThreadManager () {
	if (running) {
		running = false;
		sync();
	}
	pthread_mutex_destroy(&mutex0);
	pthread_mutex_destroy(&mutex1);
	pthread_mutex_destroy(&mutex2);
	delete []threads;
}

void ThreadManager::sync()
{
	//printf("running_jobs = %d\n", running_jobs);
	while (running_jobs > 0) { usleep(10); }
	running = false;
	for (int i = 0;i < thread_num;i++) {
		pthread_join(threads[i], NULL);
	}
}

int ThreadManager::size()
{
	return running_jobs;
}

void ThreadManager::worker()
{
	while (running) {
		int rc = pthread_mutex_trylock(&mutex0);
		if (!rc) {
			Job ajob;
			if (jobs.size() > 0) {
				ajob = jobs.front();
				jobs.pop();
			}
			pthread_mutex_unlock(&mutex0); 

			if (ajob.task) { //succ acquire a Job
				ajob.task(ajob.arg);

				pthread_mutex_lock(&mutex2);
				running_jobs --;
				pthread_mutex_unlock(&mutex2); 
			} 


		}else { usleep(1); }
		usleep(1);
	}
}

int ThreadManager::append(void *(*task)(void*), void *real)
{
	while (jobs.size() > 10000) { usleep(1); }
	pthread_mutex_lock(&mutex0); 
	jobs.push(Job(task, real));
	pthread_mutex_unlock(&mutex0);
	
	pthread_mutex_lock(&mutex2);
	running_jobs ++;
	pthread_mutex_unlock(&mutex2);
	return true;
}

