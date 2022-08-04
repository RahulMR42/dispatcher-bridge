updatedynamooutputs(lambdafuncname) # Updates transactions in dynamodb
  ### GENERATED CODE
  

  message = 'start_benchmark= {}, dynamodbtable= {}'.format(event['input1'], event['lambdafuncname'])  
  return { 
    'message' : message
  }