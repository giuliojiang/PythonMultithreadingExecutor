import threading
import time

# ==============================================================================
# The queue where the jobs data is stored
# a JobsQueue object is shared among the threads
class JobsQueue (object):
    
    def __init__(self, datalist):
        self.datalist = datalist
        self.i = 0
    
    def isEmpty(self):
        return self.i == len(self.datalist)
    
    def get(self):
        result = self.datalist[self.i]
        self.i += 1
        return result
    
    def size(self):
        return len(self.datalist)
        
# ==============================================================================
# An execution thread. It will pull jobs from
# the queue and execute
class ExecutorThread (threading.Thread):
    
    def __init__(self, jobsqueue, jobsqueuelock, applyfunction):
        threading.Thread.__init__(self)
        self.jobsqueue = jobsqueue
        self.jobsqueuelock = jobsqueuelock
        self.applyfunction = applyfunction
    
    def run(self):
        while True:
            # acquire lock
            self.jobsqueuelock.acquire()
            # get data
            data = None
            if self.jobsqueue.isEmpty():
                self.jobsqueuelock.release()
                break
            else:
                data = self.jobsqueue.get()
            # release lock
            self.jobsqueuelock.release()
            # run the function
            self.applyfunction.f(data)

# ==============================================================================
# returns a new explicit lock
def get_new_lock():
    return threading.Lock()

# ==============================================================================
# Asynchronous map
def map_async(applyfunction, data, ncpus):
    
    # construct queue and lock
    theQueue = JobsQueue(data)
    queuelock = get_new_lock()

    # create executor threads
    executors = []
    for i in range(ncpus):
        anExecutor = ExecutorThread(theQueue, queuelock, applyfunction)
        executors.append(anExecutor)

    # start threads
    for e in executors:
        e.start()

    # while there are jobs to be done, wait
    while not (theQueue.isEmpty()):
        time.sleep(0.016)

    # stop threads
    for e in executors:
        e.join()
    
    return
