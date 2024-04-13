import boto3

iam = boto3.client('iam')

username = input("Enter username: ")

# Create the user
iam.create_user(UserName=username)
print(f"Created user {username}")

create_key = input(f"Create access key for {username}? (y/n) ")

if create_key.lower() == "y":
  response = iam.create_access_key(UserName=username)
  print("Access key created")
