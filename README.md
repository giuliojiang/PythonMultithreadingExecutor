# MultiThreadedExecutor

A multiprocessing async_map alternative based on threads.

This is thought as an alternative to python's async_map in the multiprocessing module. While multiprocessing is a great tool, there are several disadvantages: the overhead of processes is quite high compared to threads, and sharing data among processes is very difficult.

This multithreading executor module tries to replicate the basic functionalities of async_map, while providing the advantages of threads. It is possible to share data among threads, and to get return values by simply modifying the data parameter that is passed to the function.

# Usage

The MultiThreadedExecutor is extremely easy to use:

1 - save mtexecutor.py to your project directory

2 - import mtexecutor

3 - create the apply function. A template is the following:
```
class MyF (object):
    
    def __init__(self):
        pass
    
    def f(self, data):
        # the calculation you want to do on the data
        pass
```

4 - prepare the data you want to process as a python list

5 - call mtexecutor.map_async(theFunction, data, ncpus), where theFunction is the instance of the function class you want to apply, data is a list of data to be processed, and ncpus is the number of threads to be instantiated.

An example of usage is found in https://github.com/giuliojiang/PythonMultithreadingExecutor/blob/master/test.py

# Implementation

The list of data is used to construct a queue of jobs. A number of threads equal to the specified number of cpus is created.

Each thread will retrieve jobs from the head of the queue and apply the function asynchronously. Once the queue is empty, the thread joins and map returns.

# Shared objects

A major advantage of MultiThreadedExecutor over the multiprocessing module is the possibility to easily share data among threads. A simple way to share an object, is to have each data element in the jobs list to be a tuple, with all the tuples sharing an object.

Explicit locks can be obtained with
```
alock = mtexecutor.get_new_lock()
```
to control the access to the shared object(s)
```
alock.acquire()
# operations
alock.release()
```
