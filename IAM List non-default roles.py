import boto3

iam = boto3.client('iam')

default_roles = ['AWSReservedSSO_Role', 'AWSServiceRoleForOrganizations']

def list_roles(marker=None):

  params = {'MaxItems': 25}
  if marker:
    params['Marker'] = marker

  response = iam.list_roles(**params)

  roles = response['Roles']

  print("Non-Default Roles:")
  for role in roles:
    if role['RoleName'] not in default_roles and not role['Arn'].startswith('arn:aws:iam::aws:role/'):
      print(f"- {role['RoleName']}")

  if 'Marker' in response:
    print("Listing more roles...")
    list_roles(response['Marker'])

print("Listing non-default roles...")
list_roles()
