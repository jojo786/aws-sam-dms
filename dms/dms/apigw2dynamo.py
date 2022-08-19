import json
import boto3
import os


document_table = os.environ["DocumentTable"]
client = boto3.client('dynamodb')

def lambda_handler(event, context):
  #print(event)
  query = event['queryStringParameters']
  print(query)
  data = client.get_item(
    TableName=document_table,
     Key={
        'dms_id': {
            'S':'DMS-34533452'
            }, 
        'document':{
            'S': 'id-pic.jpg'
            } 
    }
  )

  response = {
      'statusCode': 200,
      'body': json.dumps(data),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
  }
  
  return response