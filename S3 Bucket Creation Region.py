import logging
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

bucket_name = input("Enter bucket name: ")
bucket_region = input("Enter bucket region: ")

try:
  response = s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
      'LocationConstraint': bucket_region
    }
  )
  
  print(f"Bucket {bucket_name} created successfully.")
  
except s3.exceptions.BucketAlreadyOwnedByYou as e:
  new_name = input(f"Bucket {bucket_name} already exists, enter a new name: ")
  bucket_name = new_name
  response = s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
      'LocationConstraint': bucket_region
    }
  )
  print(f"Bucket {bucket_name} created successfully.")
  
except Exception as e:
  print("An error occurred:", e)
