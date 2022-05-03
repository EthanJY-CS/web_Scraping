import boto3

def upload_to_s3(fileName, bucketName, objectName):
    s3_client = boto3.client('s3')
    #response = s3_client.upload_file(file_name, bucket, object_name)
    response = s3_client.upload_file(fileName, bucketName, objectName)

def view_bucket_contents(bucketName):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucketName)
    for file in my_bucket.objects.all():
        print(file.key)

def download_files(bucketName, objectName, fileName):
    s3 = boto3.client('s3')
    # Of course, change the names of the files to match your own.
    s3.download_file(bucketName, objectName, fileName)

