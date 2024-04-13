import boto3

iam = boto3.client('iam')

keyword = input("Enter the keyword to search for: ")

policies_to_process = iam.list_policies(Scope='Local',OnlyAttached=False)
matching_policies = []

for policy in policies_to_process['Policies']:
  if keyword in policy['PolicyName']:
    matching_policies.append(policy)

num_pages = int(len(matching_policies)/25) + 1
for page in range(num_pages):
  start_index = page*25
  end_index = min((page+1)*25, len(matching_policies))
  print(f"Policies {start_index} to {end_index}:")
  for policy in matching_policies[start_index:end_index]:
    print(f"- {policy['PolicyName']}")

  action = input("Do you want to keep or delete these policies? (keep/delete): ")

  if action == "delete":
    confirm = input("Are you sure you want to delete these policies? Type 'yes' to confirm: ")
    if confirm == "yes": 
      for policy in matching_policies[start_index:end_index]:
        iam.delete_policy(PolicyArn=policy['Arn'])
        print(f"Deleted policy {policy['PolicyName']}")
    else:
      print("Policy deletion cancelled")
