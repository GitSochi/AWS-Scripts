import boto3

iam = boto3.client('iam')

def list_roles(marker=None):

  params = {'MaxItems': 25}
  if marker:
    params['Marker'] = marker

  response = iam.list_roles(**params)

  roles = response['Roles']

  print("Roles:")
  for role in roles:
    print(f"- {role['RoleName']}")

  if 'Marker' in response:
    print("Listing more roles...")  
    list_roles(response['Marker'])

print("Listing roles...")
list_roles()
