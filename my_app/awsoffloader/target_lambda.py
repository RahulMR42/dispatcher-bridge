#!/usr/bin/python3
import boto3, json
# lambda_client = boto3.client('lambda')

import time
import platform
#from cpuinfo import get_cpu_info
#from threading import Thread
from botocore.exceptions import ClientError
from decimal import Decimal


### GENERATED CODE
def updatedynamooutputs(db_name):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(db_name)
  try:
    response = table.update_item(Key={'outputs': 'output1'},
  ###REPLICATE THE LOGIC TO UPDATE THE VARIABLE
  #"transactions = transactions+1">>'SET outputvalue = outputvalue + :inc'
    UpdateExpression='SET outputvalue = outputvalue + :inc',
    ExpressionAttributeValues={
        ':inc': Decimal(1)
    },
    ReturnValues="UPDATED_NEW"
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
### GENERATED CODE

def lambda_handler(event, context):
  start_benchmark= int(event['input1'])
  lambdafuncname=event['lambdafuncname']
  
  
  #start-movetocloud#
  for i in range(0,start_benchmark):
    for x in range(1,1000):
      3.141592 * 2**x
    for x in range(1,10000):
      float(x) / 3.141592
    for x in range(1,10000):
      float(3.141592) / x
  updatedynamooutputs('dispatch-Tk48zHkf3cJf3GTXW7zcqN') # Updates transactions in dynamodb
  ### GENERATED CODE
  
# message = 'start_benchmark= {}, dynamodbtable= {}'.format(event['input1'], event['lambdafuncname'])  
# return { 
#     'message' : message
#   }