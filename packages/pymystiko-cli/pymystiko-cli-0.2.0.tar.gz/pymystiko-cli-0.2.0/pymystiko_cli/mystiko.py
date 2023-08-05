import collections
import json
import os
import subprocess
import tempfile

from botocore.exceptions import ClientError

from fnmatch import fnmatch
from jsonschema import validate

from . import aws


class MystikoContext:
    def __init__(self, options, env, ctx):
        self.options = options
        self.env = env
        self.ctx = ctx

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        envs = self.ctx['envs']
        for k in envs:
            del self.env[k]
        files = self.ctx['files']
        for f in files:
            os.unlink(f)



def _extend(dct, merge_dct):
    d = dict(**dct)
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            d[k] = _extend(dct[k], merge_dct[k])
        else:
            d[k] = merge_dct[k]
    return d


def extend(*args):
    """
    Extends dictionaries (base, added1, added2)
    :param args:
    :return: Dictionary
    """
    dct = args[0]
    idx = 1
    while idx < len(args):
        dct = _extend(dct, args[idx])
        idx += 1
    return dct


def mystiko(options, env=dict(os.environ)):
    ctx = {
        'envs': [],
        'files': []
    }
    current_env = get_environment(options)
    sm_client = aws.get_client('secretsmanager', env, current_env)

    load_environment(current_env, env, sm_client, ctx, options.get('filter', None))

    return MystikoContext(options, env, ctx)


def format_secret_name(secret_name, current_env):
    if 'secretNamePrefix' in current_env:
        return format_with_parameters(current_env['secretNamePrefix'] + secret_name['name'], current_env)
    return format_with_parameters(secret_name['name'], current_env)


# def add_secret(options, client):
#     secret_env = get_environment(options)
#
#     secret_name = format_secret_name(options['name'], secret_env)
#     secret_value = options['value']
#
#     aws.add_secret({
#         'name': secret_name,
#         'value': secret_value
#     }, client)


def list_secrets(mystiko_options, env):
    current_env = get_environment(mystiko_options)
    sm_client = aws.get_client('secretsmanager', env, current_env)

    prefix = format_with_parameters(current_env.get('secretNamePrefix', ''), current_env)
    if prefix:
        list_opts = {
            'filters': [{'Key': 'name', 'Values': [prefix]}]
        }
    else:
        list_opts = {}

    secrets = aws.list_secrets(list_opts, sm_client)['SecretList']

    for secret in secrets:
        yield {
            'name': secret['Name']
        }


def get_environment(options):
    config_file = os.path.realpath(options.get('configFile', None) or '.mystiko')
    config = read_file(config_file)

    environments = config.get('environments', {})
    defaults = config.get('defaults', None)
    current_env_name = options.get('env', 'local')
    current_env = environments.get(current_env_name, {})

    if defaults:
        secrets = list(defaults.get('secrets', []))
        secrets += current_env.get('secrets', [])
        current_env = extend(defaults, current_env)
        current_env['secrets'] = secrets

    return current_env


def add_secret(options, mystiko_options, env):
    current_env = get_environment(mystiko_options)
    sm_client = aws.get_client('secretsmanager', env, current_env)
    try:
        options['name'] = format_secret_name(options, current_env)
        return {
            'action': 'added',
            'resp': aws.add_secret(options, sm_client)
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException' and options.get('upsert', False):
            return {
                'action': 'updated',
                'resp': aws.update_secret(options, sm_client)
            }
        else:
            raise


def update_secret(options, mystiko_options, env):
    current_env = get_environment(mystiko_options)
    sm_client = aws.get_client('secretsmanager', env, current_env)

    try:
        options['name'] = format_secret_name(options, current_env)
        return {
                'action': 'updated',
                'resp': aws.update_secret(options, sm_client)
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException' and options.get('upsert', False):
            return {
                'action': 'added',
                'resp': aws.add_secret(options, sm_client)
            }
        else:
            raise


def delete_secret(options, mystiko_options, env):
    current_env = get_environment(mystiko_options)
    sm_client = aws.get_client('secretsmanager', env, current_env)

    options['name'] = format_secret_name(options, current_env)
    resp = aws.delete_secret(options, sm_client)
    return resp


def get_secret(options, mystiko_options, env):
    current_env = get_environment(mystiko_options)
    sm_client = aws.get_client('secretsmanager', env, current_env)

    options['name'] = format_secret_name(options, current_env)
    resp = aws.get_secret(options, sm_client)
    return resp


def execute(options, mystiko_options, env):
    with mystiko(mystiko_options, env=env):
        tmpfile = tempfile.mktemp()
        with open(tmpfile, 'w') as fhd:
            fhd.write(options['command'])
        command_list = [
            '/bin/bash',
            '-e',
            tmpfile
        ]
        rc = subprocess.check_call(command_list, env=env)
    return rc


# def save_file(options, config_file, config):
#     config_file = os.path.realpath(options.get('configFile', '.mystiko'))
#     config = read_file(config_file)



#
# def validate_schema(config, schema):
#     validate(instance=config, schema=schema)


def format_with_parameters(value: str, current_env: dict):
    parameters = current_env.get('parameters', {})
    return value.format(**parameters)


def populate_secret(secret, current_env, secret_value, target_env, ctx):
    if 'keyValues' in secret:
        secret_json = json.loads(secret_value)
        key_values = secret['keyValues']
        for key_value in key_values:
            key_name = format_with_parameters(key_value['key'], current_env)
            json_value = secret_json[key_name]
            populate_secret(key_value, current_env, json_value, target_env, ctx)
    elif 'envname' in secret:
        envname = format_with_parameters(secret['envname'], current_env)
        ctx['envs'].append(envname)
        target_env[envname] = secret_value
    elif 'filename' in secret:
        filename = os.path.realpath(format_with_parameters(secret['filename'], current_env))
        ctx['files'].append(filename)
        with open(filename, 'w') as fhd:
            fhd.write(secret_value)


def load_secret(secret, current_env, sm_client, target_env, ctx, filter):
    name = format_secret_name(secret, current_env)
    if not filter or fnmatch(name, filter):
        secret_value = aws.get_secret({
            'name': name
        }, sm_client)
        populate_secret(secret, current_env, secret_value['SecretString'], target_env, ctx)


def load_environment(current_env, env, sm_client, ctx, filter):
    secrets = current_env.get('secrets', [])

    for secret in secrets:
        load_secret(secret, current_env, sm_client, env, ctx, filter)


def read_file(path):
    if os.path.exists(path):
        with open(path, 'rb') as fhd:
            return json.load(fhd)
    return {}
