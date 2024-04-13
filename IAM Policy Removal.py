import boto3

iam = boto3.client('iam')

def remove_attached_policies(role_name):

  policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

  if policies:
    print(f"Removing {len(policies)} policies from role {role_name}")
    for policy in policies:
      policy_arn = policy['PolicyArn']  
      iam.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
      print(f"Detached policy {policy_arn}")
  else:
    print(f"No policies attached to role {role_name}")

if __name__ == '__main__':

  role_name = input("Enter IAM role name: ")

  remove_attached_policies(role_name)
