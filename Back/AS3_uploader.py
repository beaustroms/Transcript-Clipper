import filestack
import os

s3_client = filestack.Client('s3', region_name='us-east-1', aws_access_key_id=os.environ["AS3_Secret"],                       

aws_secret_access_key=os.environ["AS3_Secret"])

def upload_file(bucket, folder, file_to_upload, file_name):
    file = folder+"/"+file_name
    try:
        s3_client.upload_file(file_to_upload, bucket, file)
    except Exception as e:
        print(e)
        return False
    return True  

# Variables 1 and 2 are for you to enter