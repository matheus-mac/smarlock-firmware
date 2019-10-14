import logging
import boto3
from botocore.exceptions import ClientError

client = boto3.client(
    's3',
    aws_access_key_id='AKIARXPQXYQ5TIUVFSFH',
    aws_secret_access_key='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'
)
link = "https://smartlock-filebucket.s3-us-west-2.amazonaws.com/"

def upload_file(file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    #s3 = boto3.client('s3')
    try:
        response = client.upload_file(file_name, "smartlock-filebucket", file_name)
        return(link + file_name)
    except ClientError as e:
        logging.error(e)
        return "Falha no upload"

def download_file(file_name):
    client.download_file("smartlock-filebucket", file_name, file_name)