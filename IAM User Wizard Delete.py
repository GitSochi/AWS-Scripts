import boto3

def remove_user(username):

  iam = boto3.client('iam')

  # Remove access key if it exists
  try:
    response = iam.list_access_keys(UserName=username)
    access_key = response['AccessKeyMetadata'][0]['AccessKeyId']
    iam.delete_access_key(UserName=username, AccessKeyId=access_key)
  except (iam.exceptions.NoSuchEntityException, IndexError):
    pass

  # Detach any attached policies
  try:
    response = iam.list_attached_user_policies(UserName=username)
    for policy in response['AttachedPolicies']:
      iam.detach_user_policy(
        UserName=username, 
        PolicyArn=policy['PolicyArn']
      )
  except iam.exceptions.NoSuchEntityException:
    pass

  # Delete the user
  iam.delete_user(UserName=username)

  print(f"Removed access for user {username}")

if __name__ == '__main__':
  username = input("Enter username: ")
  remove_user(username)
