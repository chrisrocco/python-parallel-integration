import math
import time
from queue import Queue
from threading import Thread
# I(func) = integ(func, a, b)

NUM_WORKERS = 4
task_queue = Queue()
I = 0

def area(func, a, b, tol):
    S = []
    S.append((a,b))
    global I
    while S:
        a, b = S.pop() # the interval (a, b) popped
        I1 = ((b-a)/2)*(func(a)+func(b)) # trapezoid rule
        m = (a + b)/2
        I2 = ((b-a)/4)*(func(a) + func(b) + 2*func(m)) # composite trapezoid rule with 2 subintervals
        if abs(I1-I2) < 3*(b-a)*tol:
            I += I2
        else:
            S.append((a, m))
            S.append((m, b))
    
def esinx(x):
    return math.exp(3*x)*math.sin(2*x)

a = 0
b = math.pi/4
xPoints = []
for i in range(NUM_WORKERS):
    xPoints.append(a + i*(b-a)/4)
xPoints.append(b)
# Create the worker threads
start_time = time.time()
threads = [Thread(target=area(esinx, xPoints[i], xPoints[i+1], (math.pi/4)*.0001)) for i in range(NUM_WORKERS)]
# for thread in threads:
#     print(thread.start())
[thread.start() for thread in threads]
[thread.join() for thread in threads]
print(I)
end_time = time.time()



print("the time it took is", end_time - start_time, "seconds")
