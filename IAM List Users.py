import boto3

iam = boto3.client('iam')

response = iam.list_users()
users = response['Users']

print("IAM Users:")
for user in users:
    print(f"- {user['UserName']}")
