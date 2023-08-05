import boto3
import json

from botocore.exceptions import ClientError


def assume_role(aws_env, current_env):
    sts = _get_client('sts', aws_env, current_env)

    assume_role_params = {
        'RoleArn': current_env.get('roleArn'),
        'RoleSessionName': current_env.get('session_name', 'mystiko'),
        'DurationSeconds': current_env.get('duration_seconds', 3600)
    }

    result = sts.assume_role(**assume_role_params)

    credentials = result['Credentials']
    return {
        'AWS_ACCESS_KEY_ID': credentials['AccessKeyId'],
        'AWS_SECRET_ACCESS_KEY': credentials['SecretAccessKey'],
        'AWS_SESSION_TOKEN': credentials['SessionToken']
    }


def _get_client(client_name, aws_env, current_env):
    profileName = None
    if 'AWS_ACCESS_KEY_ID' not in aws_env:
        profileName = current_env.get('profileName', aws_env.get('AWS_PROFILE', None))
    session = boto3.session.Session(
        aws_access_key_id=aws_env.get('AWS_ACCESS_KEY_ID', None),
        aws_secret_access_key=aws_env.get('AWS_SECRET_ACCESS_KEY', None),
        aws_session_token=aws_env.get('AWS_SESSION_TOKEN', None),
        profile_name=profileName,
        region_name=current_env.get('region', aws_env.get('AWS_DEFAULT_REGION', 'us-west-2'))
    )
    return session.client(client_name)


def get_client(client_name, aws_env, current_env):
    if 'roleArn' in current_env:
        aws_env = assume_role(current_env, aws_env)

    return _get_client(client_name, aws_env, current_env)


def add_secret(options, client):
    response = client.create_secret(
        Name=options['name'],
        Description=options.get('description', ''),
        SecretString=options['value'],
        Tags=options.get('tags', [])
    )
    return response


def update_secret(options, client):
    response = client.put_secret_value(
        SecretId=options['name'],
        SecretString=options['value']
    )
    return response


def delete_secret(options, client):
    response = client.delete_secret(
        SecretId=options['name'],
        ForceDeleteWithoutRecovery=options.get('force', False)
    )
    return response


def get_secret(options, client):
    response = client.get_secret_value(
        SecretId=options['name']
    )
    return response


def list_secrets(options, client):
    response = client.list_secrets(
        Filters=options.get('filters', []),
        MaxResults=100
    )
    return response
