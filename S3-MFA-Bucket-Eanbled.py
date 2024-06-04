### This is a Custom Config Lambda Rule, that evaluates the Config rule based off the s3-mfa-bucket-delete-enabled Config Rule, it will also update the compliance status in Config ###

import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Create an AWS Config client
    config_client = boto3.client('config')

    # Get the result token from the event, if available
    result_token = event.get('resultToken', None)

    # Get a list of all S3 buckets
    response = s3.list_buckets()
    buckets = response['Buckets']

    # Check the MFA delete status for each bucket
    evaluations = []
    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            # Get the bucket versioning configuration
            versioning = s3.get_bucket_versioning(Bucket=bucket_name)
            if 'MFADelete' in versioning:
                mfa_delete_status = versioning['MFADelete']
                if mfa_delete_status == 'Enabled':
                    compliance_type = 'COMPLIANT'
                else:
                    compliance_type = 'NON_COMPLIANT'
            else:
                compliance_type = 'NON_COMPLIANT'

            # Create an evaluation
            evaluation = {
                'ComplianceResourceType': 'AWS::S3::Bucket',
                'ComplianceResourceId': bucket['Name'],
                'ComplianceType': compliance_type,
                'OrderingTimestamp': datetime.now()
            }
            evaluations.append(evaluation)

            print(f"Bucket: {bucket['Name']}, MFA Delete: {mfa_delete_status if 'mfa_delete_status' in locals() else 'Not Set'}, Compliance: {compliance_type}")
        except Exception as e:
            print(f"Error checking bucket '{bucket['Name']}': {e}")

    # Report evaluations to AWS Config
    if result_token:
        try:
            config_client.put_evaluations(
                Evaluations=evaluations,
                ResultToken=result_token
            )
            print(f"AWS Config put_evaluations response: {response}")
        except Exception as e:
            print(f"Error reporting evaluations to AWS Config: {e}")

    return {
        'statusCode': 200,
        'body': {
            'message': 'Evaluations reported to AWS Config'
        }
    }
