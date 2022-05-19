import boto3
import os
from sqlalchemy import create_engine
import pandas as pd

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'gymshark-database.cealtvnlvdai.eu-west-1.rds.amazonaws.com' # Change it for your AWS endpoint
USER = 'postgres'
PASSWORD = 'EthanJY69' 
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

def upload_to_s3(fileName, bucketName, objectName):
    s3_client = boto3.client('s3', aws_access_key_id="AKIA3W5XCOYOUCF6QDXX",
         aws_secret_access_key="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")
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

def upload_directory_to_s3():
    s3_client = boto3.client('s3')
    try:
        root_path = "/home/ethanjy/Scratch/web_Scraping/raw_data" # local folder for upload
        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = path.replace(root_path,"")
            for file in files:
                s3_client.upload_file(os.path.join(path, file), "gymshark-data", directory_name+'/'+file)
    except Exception as err:
        print(err)

def add_record_to_rds(dict_ToAdd):
    with engine.connect() as connection:
        record = pd.DataFrame([dict_ToAdd])
        record.to_sql("gymshark_database", connection, if_exists='append')

def read_database():
    with engine.connect() as connection:
        df = pd.read_sql_table("gymshark_database", connection)
        print(df.loc[:,['ID']].head())
        print(df.shape)

def does_record_exist(id):
    with engine.connect() as connection:
        record = connection.execute('SELECT 1 FROM gymshark_database WHERE "ID" = %s;', id)
        if record.rowcount == 0:
            return False
        else:
            return True

def drop_table():
    with engine.connect() as connection:
        connection.execute('DROP TABLE gymshark_database;')

if __name__ == '__main__':
    drop_table()
