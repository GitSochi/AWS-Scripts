import boto3

iam = boto3.client('iam')

def remove_attached_policies(username):

  policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']

  if policies:
    print(f"Removing {len(policies)} policies from user {username}")
    for policy in policies:
      policy_arn = policy['PolicyArn']
      iam.detach_user_policy(UserName=username, PolicyArn=policy_arn) 
      print(f"Detached policy {policy_arn}")
  else:
    print(f"No policies attached to user {username}")

if __name__ == '__main__':

  username = input("Enter IAM username: ")

  remove_attached_policies(username)
