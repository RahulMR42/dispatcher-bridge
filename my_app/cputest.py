#!/usr/bin/python3
#Python CPU Benchmark by Alex Dedyura (Windows, macOS, Linux)

import time
import platform
from cpuinfo import get_cpu_info
from threading import Thread


os_version = platform.system()

print('Python CPU Benchmark by Fahd')
info = get_cpu_info()
print('CPU: ' + info.get('brand_raw'))
print('Arch: ' + info.get('arch_string_raw'))
print('OS: ' + str(os_version))

start_benchmark = 100 # change this if you like (sample: 1000, 5000, etc)
start_benchmark = int(start_benchmark)
numtrans = 100 # attemps, change this if you like (sample: 3, 5, etc)
numtrans = int(numtrans)
average_benchmark = 0
threads = []
tgtperfpermin=60
runbenchmark = 0
runbenchmark = int(runbenchmark)
transactions = 0
newthreadstocreate = 0
newthreadstocreate = int(newthreadstocreate)
oldtransactions = 0
initthreads=50

def task(id):
  global transactions
#start-movetocloud#
  for i in range(0,start_benchmark):
    for x in range(1,1000):
      3.141592 * 2**x
    for x in range(1,10000):
      float(x) / 3.141592
    for x in range(1,10000):
      float(3.141592) / x
#end-movetocloud#
  transactions = transactions+1


def createthreads(numthreads):
#  print('creating ' + str(numthreads) + ' threads to handle transactions')
  for a in range(0,numthreads):
    t = Thread(target=task, args=(a,))
    threads.append(t)
    # start the threads
    t.start()
  print('created '+ str(numthreads) + ' new threads')
  
print('starting benchmark now')
start = time.time()
createthreads(initthreads)

while transactions < numtrans:
  end = time.time()
  duration = (end - start)
  performance = 60*transactions/duration
  duration = round(duration, 3)
  performance = round(performance, 3)
  print('Transactions = ' + str(transactions) + '. Performance  = ' + str(performance) + ' Transactions per minute')
  newthreadstocreate=transactions-oldtransactions
  oldtransactions=transactions
  createthreads(newthreadstocreate)
  time.sleep(1)
  
end = time.time()
duration = (end - start)
performance = 60*transactions/duration
duration = round(duration, 3)
performance = round(performance, 3)
#print('Transactions = ' + str(transactions) + '. Performance  = ' + str(performance) + ' Transactions per minute')
print('Total Time: ' + str(duration) + 's. transactions ' + str(transactions) + '. Performance  ' + str(performance) + ' Transactions per minute')
  
# wait for the threads to complete
for t in threads:
    t.join()
# #testoffload#
# average_benchmark = round(average_benchmark / repeat_benchmark, 3)
# print('Average (from 10 repeats): ' + str(average_benchmark) + 's')