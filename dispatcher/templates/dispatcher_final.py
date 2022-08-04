#!/usr/bin/python3
#Python CPU Benchmark by Alex Dedyura (Windows, macOS, Linux)


import boto3, json
lambda_client = boto3.client('lambda')


import time
import platform
from cpuinfo import get_cpu_info
from threading import Thread
from botocore.exceptions import ClientError
from decimal import Decimal

os_version = platform.system()

print('Python CPU Benchmark by RahulMR & FahdA')
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


#INSERTEDINITCODE
appname='dispatch-SID'
def deldynamooutputs(lambdafuncname,dynamodb=None):
    #print('Creating DynamoBDTable connection')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(lambdafuncname)
    table.delete()
    
# def createynamooutputs(lambdafuncname,dynamodb=None):
#     if not dynamodb:
# #        print('Creating DynamoBDTable connection')
#         dynamodb = boto3.resource('dynamodb')
# #    print('Connection creates, now creatomg a Table')
#     table = dynamodb.create_table(
#         TableName=lambdafuncname,
#         KeySchema=[
#           {
#             'AttributeName': 'outputs',
#             'KeyType': 'HASH'  # Partition key
#           },
#         ],
#         AttributeDefinitions=[
#           {
#             'AttributeName': 'outputs',
#             'AttributeType': 'S'
#           },
#         ],
#         ProvisionedThroughput={
#           'ReadCapacityUnits': 10,
#           'WriteCapacityUnits': 10
#         }
#     )

# #    print('Table created, now adding values to table')
#     time.sleep(10)
#     response = table.put_item(
#       Item={
#             'outputs': 'output1',
#             'outputvalue': 0
#             }
#     )
#     time.sleep(5)

# createynamooutputs(appname,None)
#INSERTEDINITCODE

#movetocloud#
#offloads the compute logic and stores results in dynamoDB
def offloadlambafunc(lambdafuncname):
# create JSON payload:
    x = {'input1':start_benchmark, 'input2':0, 'lambdafuncname':lambdafuncname}
    pload = json.dumps(x, indent=4)
#    print('offloading to lambda')
    lamdaresponse = lambda_client.invoke(
    FunctionName= lambdafuncname,
#    InvocationType="RequestResponse",
    InvocationType='Event', #non blocking invocation
    Payload=pload
    )
    results = lamdaresponse['Payload'].read()
    #print('lambdadone')
    
#when invoked, returns dynamodb outputs
def getdynamooutputs(lambdafuncname):
  #print('Creating DynamoBDTable connection')
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(lambdafuncname)
#  print('Connection creates, now getting values')
  try:
      response = table.get_item(Key={'outputs': 'output1'})
  except ClientError as e:
      print(e.response['Error']['Message'])
  else:
#      print("Get outputs succeeded. Here is the output")
#      print(response['Item']['outputvalue'])
      output1 = int(round((response['Item']['outputvalue']), 0))
      return output1
#movetocloud#

def createthreads(numthreads):
#  print('creating ' + str(numthreads) + ' threads to handle transactions')
  for a in range(0,numthreads):
    # Substitue 
    #t = Thread(target=task, args=(a,))
    #threads.append(t)
    ## start the threads
    #t.start()
    #
    # for
    #
    offloadlambafunc(appname)
  print('created '+ str(numthreads) + ' new threads')


print('starting benchmark now')
start = time.time()
createthreads(initthreads)
##SUBSTITUTE transactions variable for getdynamooutputs(appname)
while getdynamooutputs(appname) < numtrans:
  end = time.time()
  duration = (end - start)
  performance = 60*getdynamooutputs(appname)/duration #SUBSTITUE
  duration = round(duration, 3)
  performance = round(performance, 3)
  print('Transactions = ' + str(getdynamooutputs(appname)) + '. Performance  = ' + str(performance) + ' Transactions per minute')#SUBSTITUE
  newthreadstocreate=getdynamooutputs(appname)-oldtransactions#SUBSTITUE
  oldtransactions=getdynamooutputs(appname)#SUBSTITUE
  createthreads(newthreadstocreate)
  time.sleep(1)
  
end = time.time()
duration = (end - start)
performance = 60*int(getdynamooutputs(appname))/duration
duration = round(duration, 3)
performance = round(performance, 3)
#print('Transactions = ' + str(transactions) + '. Performance  = ' + str(performance) + ' Transactions per minute')
print('Total Time: ' + str(duration) + 's. transactions ' + str(getdynamooutputs(appname)) + '. Performance  ' + str(performance) + ' Transactions per minute')
  
# wait for the threads to complete
for t in threads:
    t.join()
# #testoffload#
# average_benchmark = round(average_benchmark / repeat_benchmark, 3)
# print('Average (from 10 repeats): ' + str(average_benchmark) + 's')

#INSERTEDCLEANUPCODE
deldynamooutputs(appname,None)
#INSERTEDCLEANUPCODE