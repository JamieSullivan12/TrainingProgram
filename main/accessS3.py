#accessing AWS bucket
#import boto3
import os

def s3accesscode():

    #basic credentials 
    aws_access_key='AKIASKERJ7ZN2VU2TAVB'
    aws_secret_access = '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'

    #Connect to the AWS s3 service
    client = boto3.client(
        's3',
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_access,
        region_name = 'ap-southeast-2'
    )

    bucket_name = 'test-bucket-71'

    #uploading a file
    client.upload_file('data/test.csv', bucket_name, 'test_file.csv')

    #downloading a file
    client.download_file(bucket_name, 'test_file.csv', 'data/downloads/test_file.csv')