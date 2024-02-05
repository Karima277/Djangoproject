def func_1(array):
    return [i for i in array if i] + [0] * array.count(0)

def func_2(array):
    for i in array:
        if i == 0:
            array.remove(i)
            array.append(0)
    return array

def func_3(array):
    t=[]
    z = 0
    for i in array:
        if i != 0:
            t.append(t)
        else:
            z+=1
    return t + [0]*z

import random
import time 

n = 1_000_000_000
array = [random.randint(0, 100) for _ in range(n)]


start = time.time()
func_1(array)
print("time: ",time.time() - start)

# start = time.time()
# func_2(array)
# print("time: ",time.time() - start)

start = time.time()
func_3(array)
print("time: ",time.time() - start)

# result for n = 1_000_000
# time 1 :  0.05193924903869629
# time 2 :  106.86313700675964
# time 3 :  0.056962013244628906
