
import re
import os
import boto3
import json
import shortuuid
import shutil
import itertools
import logging
from pathlib import Path
from colorama import init, Fore, Back, Style


### Variables

SUID = shortuuid.uuid()
FILENAME = r'../my_app/cputest.py'
AWS_OFFLOADER_PATH = "../my_app/awsoffloader"
OP_ATTRIBUTE = "outputs"
TEMPLATE_PATH = "templates"
AWS_ROLE_ID = "arn:aws:iam::138472308340:role/lamdbarole"
# "arn:aws:iam::138472308340:role/service-role/mr-python-function-1-role-ueboedac"
TIMEOUT_VALUE = 900
LAMBDA_HANDLER_DEFAULT = "target_lambda.lambda_handler"


### Logging configuration

logging.basicConfig(
            format='%(asctime)s - %(name)s -  %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("dispatcher.log"),
                logging.StreamHandler()
            ]
        )
        
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Starting dispatcher - AWS ")

### Config OP
shutil.rmtree(AWS_OFFLOADER_PATH, ignore_errors=True)
Path(AWS_OFFLOADER_PATH).mkdir(parents=True, exist_ok=True)

# Initializes Colorama
init(autoreset=True)

###Dynamo DB Action
dynamo_client = boto3.resource('dynamodb')
logger.info(f"Creating state store  dispatch-{SUID}")
table = dynamo_client.create_table(
     TableName= f"dispatch-{SUID}",
     KeySchema=[
          {
            'AttributeName': OP_ATTRIBUTE,
            'KeyType': 'HASH'  # Partition key
          },
        ],
        AttributeDefinitions=[
          {
            'AttributeName': OP_ATTRIBUTE,
            'AttributeType': 'S'
          },
        ],
        ProvisionedThroughput={
          'ReadCapacityUnits': 50,
          'WriteCapacityUnits': 50
        }
     
    )
table.wait_until_exists()
logger.info(f"Created a db -  dispatch-{SUID}")
response = table.put_item(
      Item={
            'outputs': 'output1',
            'outputvalue': 0
            }
    )


### Create lambda template 

with open(f"{TEMPLATE_PATH}/lambda_import.py") as f:
    with open(f"{AWS_OFFLOADER_PATH}/target_lambda.py", "w") as f1:
        for line in f:
                f1.write(line) 

### Extract Content


with open(FILENAME) as fp:
    result = list(itertools.takewhile(lambda x: '#end-movetocloud#' not in x, 
        itertools.dropwhile(lambda x: '#start-movetocloud#' not in x, fp)))

with open(f"{AWS_OFFLOADER_PATH}/target_lambda.py", "a") as f1:
        for line in result:
                f1.write(line)

### Create lambda template 

with open(f"{TEMPLATE_PATH}/lambda_dynamo.py") as f:
    with open(f"{AWS_OFFLOADER_PATH}/target_lambda.py", "a") as f1:
        for line in f:
                f1.write(line) 
                
            
### Managing template with proper values
FileName = f"{AWS_OFFLOADER_PATH}/target_lambda.py"
with open(FileName) as f:
    newText=f.read().replace('SID', SUID)

with open(FileName, "w") as f:
    f.write(newText)
    
### Making code for function

shutil.make_archive(f"{AWS_OFFLOADER_PATH}", 'zip',f"{AWS_OFFLOADER_PATH}" )
with open(f"{AWS_OFFLOADER_PATH}.zip", 'rb') as f:
                zipped_code = f.read()
    
### Making final app file

with open(f"{TEMPLATE_PATH}/dispatcher_final.py") as f:
    with open(f"{AWS_OFFLOADER_PATH}/target_app.py", "a") as f1:
        for line in f:
                f1.write(line) 
                
### Managing template with proper values
FileName = f"{AWS_OFFLOADER_PATH}/target_app.py"
with open(FileName) as f:
    newText=f.read().replace('SID', SUID)

with open(FileName, "w") as f:
    f.write(newText)
    
    
### Creating a function.

lambda_client = boto3.client('lambda')
response = lambda_client.create_function(
    FunctionName=f"dispatch-{SUID}",
    Runtime="python3.9",
    Code=dict(ZipFile=zipped_code),
    Role=AWS_ROLE_ID,
    Handler=LAMBDA_HANDLER_DEFAULT,
    Timeout=TIMEOUT_VALUE
    
    )

logger.info(f"Created a function - dispatch-{SUID} ")

print(Style.BRIGHT + Back.GREEN + Fore.BLUE + "Apply - Success!")
            
logger.info(f"Offloaded content and moved as {AWS_OFFLOADER_PATH}/target_lambda.py")
logger.info(f"Target app code created and moved as {AWS_OFFLOADER_PATH}/target_app.py")
### Delete content
os.unlink(f"{AWS_OFFLOADER_PATH}.zip") 
# #table.delete()
# logger.info(f"Deleted db -  dispatch-{SUID}")