import boto3
import json
import os
from datetime import datetime  
import uuid
import urllib.parse
 

print('Loading function')

s3 = boto3.client('s3') 
table_name = region = os.environ['CONSENT_TABLE_NAME']

def handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and get its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print(response)
        file_content = response['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
 
        print(json_content['result'])
        #insert into dynamodb
       
        put_item_in_datastore(json_content['result'],bucket,key)
    except Exception as e:
        print(e)
        raise e


def put_item_in_datastore(contents,bucket,filename):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)

    response = table.put_item(
        Item={
            "PK": str(uuid.uuid1()),
            "SK":str(contents["Patient Name: "]),
            "consent_date": str(datetime.now()),
            "grantor": str(contents["Patient Name: "]),
            "grantee": str(contents["(recipient of medical records) "]),
            "consent_type" : "HRA-Medical Records",
            "doc_metadata" : str(contents),
            "document_location":bucket,
            "document_file_name":filename
        }
    )

    print(json.dumps(response, indent=2))

              
