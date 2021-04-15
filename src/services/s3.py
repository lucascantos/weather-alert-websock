import boto3
import json
import os
from datetime import datetime

BUCKETNAME = os.environ.get('S3_BUCKET')

def s3_upload(data):
    ''' Faz upload de arquivo para o buket s3 '''
    filepath = "clients_connected.json"

    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKETNAME, Key=filepath, Body=json.dumps(data))
    print('File sent to Bucket')

def s3_download(filepath="clients_connected.json"):
    ''' Faz download de arquivo para o buket s3 '''

    s3 = boto3.client('s3')
    file_object = s3.get_object(Bucket=BUCKETNAME, Key=filepath) 
    filedata = file_object['Body'].read()
    content = json.loads(filedata)
    return content

