#!/usr/bin/env python

import mtexecutor
import time

# The kind of data on which the map will be applied. This data
# can be anything: objects, lists, tuples. The data is readable
# and writable during the process, and can therefore be used as
# output as well
class Integer (object):
    
    def __init__(self, n):
        self.n = n
        
    def __str__(self):
        return str(self.n)
    
    def __repr__(self):
        return self.__str__()

# The function that will be applied to the list
# This class must define a method f(self, data)
# which will be called by the executor
class MyF (object):
    
    def __init__(self):
        pass
    
    def f(self, data):
        data.n = data.n + 1
        time.sleep(1) # artificially increase time needed



data = []
for i in range(10):
    d = Integer(i)
    data.append(d)

print(data)

theFunction = MyF()

# Call the map_async using 8 threads
mtexecutor.map_async(theFunction, data, 8)

print(data)