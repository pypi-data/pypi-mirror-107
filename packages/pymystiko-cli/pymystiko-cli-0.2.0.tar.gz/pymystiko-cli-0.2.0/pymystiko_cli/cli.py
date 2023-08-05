import json
import os

from . import __version__ as VERSION
from . import mystiko
from . import aws

import click
import sys


def get_cli_value(value, validate):
    if value == '-':
        value = sys.stdin.read()
    if validate == "json":
        json.loads(value)
    return value


@click.command(name="add-secret", help="Add a secret to AWS Secrets Manager")
@click.pass_context
@click.option('--name', required=True, help="Name of the secret used in ASM")
@click.option('--value', required=False, help="Value of the secret")
@click.option('--upsert', is_flag=True, help="Update the secret if it already exists")
@click.option('--validate', help="Validate the value")
def add_secret(ctx, name, value, upsert, validate):
    result = mystiko.add_secret({
        'name': name,
        'value': get_cli_value(value, validate),
        'upsert': upsert
    }, ctx.obj, os.environ)
    click.echo(f"Secret {name} has been {result['action']}.")


@click.command(name="update-secret", help="Update a secret in AWS Secrets Manager")
@click.pass_context
@click.option('--name', required=True, help="Name of the secret used in ASM")
@click.option('--value', required=False, help="Value of the secret")
@click.option('--upsert', is_flag=True, help="Add secret if it does not exist")
@click.option('--validate', help="Validate the value")
def update_secret(ctx, name, value, upsert, validate):
    result = mystiko.update_secret({
        'name': name,
        'value': get_cli_value(value, validate),
        'upsert': upsert
    }, ctx.obj, os.environ)
    click.echo(f"Secret {name} has been {result['action']}.")


@click.command(name="delete-secret", help="Delete a secret in AWS Secrets Manager")
@click.pass_context
@click.option('--name', required=True, help="Name of the secret used in ASM")
@click.option('--force', is_flag=True, help="Force deletion of the secret in ASM")
def delete_secret(ctx, name, force):
    secret_prompt = click.prompt('If you are sure, type the name of the secret')
    if secret_prompt and secret_prompt == name:
        mystiko.delete_secret({
            'name': name,
            'force': force
        }, ctx.obj, os.environ)
        click.echo(f"Secret {name} has been marked for deletion.")


@click.command(name="get-secret", help="Get a secret value from AWS Secrets Manager")
@click.pass_context
@click.option('--name', required=True, help="Name of the secret used in ASM")
def get_secret(ctx, name):
    resp = mystiko.get_secret({
        'name': name
    }, ctx.obj, os.environ)
    click.echo(resp)


@click.command(name="list-secrets", help="")
@click.pass_context
def list_secrets(ctx):
    secrets = list(mystiko.list_secrets(ctx.obj, os.environ))
    click.echo('{name:<40}'.format(name='Name'))
    for secret in secrets:
        click.echo('{name:<40}'.format(**secret))


@click.command(name="exec", help="", context_settings=dict(allow_extra_args=True))
@click.pass_context
def execute(ctx):
    command = get_cli_value(' '.join(ctx.args), '')
    rc = mystiko.execute({
        'command': command
    }, ctx.obj, os.environ)
    exit(rc)


def version():
    return VERSION


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.group()
@click.pass_context
@click.option('--config')
@click.option('--env', default="local")
@click.option('--filter', default="", help="Filter secrets that are read")
@click.option('--version', is_flag=True, callback=print_version, help="Display the version.",
              expose_value=False, is_eager=True)
def main(ctx, config, env, filter):
    ctx.obj = {
        'env': env,
        'configFile': config,
        'filter': filter
    }
    pass


@click.group('aws')
@click.pass_context
def aws_group(ctx):
    pass


main.add_command(aws_group)
aws_group.add_command(add_secret)
aws_group.add_command(update_secret)
aws_group.add_command(delete_secret)
aws_group.add_command(get_secret)
aws_group.add_command(list_secrets)

main.add_command(execute)
