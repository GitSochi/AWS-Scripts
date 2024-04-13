import boto3

iam = boto3.client('iam')

# Prompt for original username
original_username = input("Enter original username: ")

# Prompt for new username  
new_username = input("Enter new username: ")

# Confirm rename  
confirm = input(f"Rename {original_username} to {new_username}? (y/n) ")

if confirm.lower() == "y":
  response = iam.update_user(
    UserName=original_username,
    NewUserName=new_username
  )
  print(f"Renamed {original_username} to {new_username}")
else:
  print("Rename cancelled")
