# -*- coding: utf-8 -*-

import base64
import shutil
import subprocess
import time
from pathlib import Path

import click
import docker

from ..client.client import APIClient
from ..commands.initializer import initialize
from ..core.app import cli
from ..core.state import pass_state
from ..helpers.deployments import prepare_docker_compose_env


@cli.command(independent=True)
@click.option('--dir', type=click.Path(resolve_path=True), default='.', prompt=True)
@click.option('--init', is_flag=True)
@pass_state
@click.pass_context
def deploy(ctx, state, dir, init):
    prepare_docker_compose_env(state=state, directory=dir)
    click.echo(f'Success deployed to {dir}')
    click.echo('If this is a new instance, then you can initialize. You need an instance token.')

    secret_path = Path(dir).joinpath('secret')
    server_token_file = Path.joinpath(secret_path, '.secret_key')

    if init:
        click.echo('Please wait...')
        click.echo('Instance starting...')
        ctx.invoke(up, dir=dir)
        time.sleep(25)

        docker_client = docker.from_env()

        click.echo('Create database...')
        container = docker_client.containers.get('testbrain-postgresql')
        container.exec_run('createdb  -h localhost -U postgres testbrain', tty=True)
        # Copy file
        testbrain_dir = Path(__file__).parent.parent.resolve()
        template_file_path = Path.joinpath(testbrain_dir, 'templates', 'postgresql.conf-tpl')
        postgresql_conf_file_path = Path(dir).joinpath('var/lib/postgresql/data/', 'postgresql.conf')
        shutil.copy(template_file_path, postgresql_conf_file_path)

        container = docker_client.containers.get('testbrain-web')
        click.echo('Apply migrations...')
        container.exec_run('python manage.py migrate --no-input', tty=True)
        click.echo('Create cache table...')
        container.exec_run('python manage.py createcachetable', tty=True)
        click.echo('Collect static files...')
        container.exec_run('python manage.py collectstatic --no-input', tty=True)

        click.echo('Instance stopping...')
        ctx.invoke(down, dir=dir)

    if not server_token_file.exists():
        click.echo('Please wait...')
        ctx.invoke(up, dir=dir)
        ctx.invoke(down, dir=dir)

    with open(server_token_file, 'rb') as f:
        token = base64.b64encode(f.read().rstrip()).decode()
        click.echo(f'Server token: {token}')

    click.echo('Success')


@cli.command(independent=True)
@click.option('--dir', type=click.Path(resolve_path=True), default='.')
@pass_state
@click.pass_context
def up(ctx, state, dir):
    docker_compose_file = Path(dir).joinpath('docker-compose.yml')
    p = subprocess.Popen(f'docker-compose -f {docker_compose_file} up -d', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if not line:
            continue
        click.echo(line.rstrip())
    p.wait()
    click.echo('Success')


@cli.command(independent=True)
@click.option('--dir', type=click.Path(resolve_path=True), default='.')
@pass_state
@click.pass_context
def down(ctx, state, dir):
    docker_compose_file = Path(dir).joinpath('docker-compose.yml')
    p = subprocess.Popen(f'docker-compose -f {docker_compose_file} down', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if not line:
            continue
        click.echo(line.rstrip())
    p.wait()
    click.echo('Success')


@cli.command(independent=True)
@click.option('--dir', type=click.Path(resolve_path=True), default='.')
@click.option('--email', required=True, prompt=True)
@click.option('--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True)
@pass_state
@click.pass_context
def deploy_with_register(ctx, state, dir, email, password):
    click.echo('Deploy...')
    ctx.invoke(deploy, dir=dir, init=True)

    click.echo('Registering...')

    result = APIClient.register(state=state, email=email, password=password)

    server_token_filename = Path(dir).joinpath('secret', '.secret_key')
    server_token_file = open(server_token_filename, 'rb')
    token = base64.b64encode(server_token_file.read().rstrip()).decode()

    state.endpoint = 'http://localhost'
    state.server_token = token
    state.api_token = result.api_key
    state.user_token = result.user_token
    state.user = {
        'id': result.id,
        'username': result.username,
        'email': result.email
    }

    license_filename = Path(dir).joinpath(f'{result.uuid}.txt')
    license_file = open(license_filename, 'w+')
    license_file.write(result.license)
    license_file.close()

    click.echo('Configuring instance...')

    ctx.invoke(up, dir=dir)
    time.sleep(20)

    ctx.invoke(initialize, endpoint=state.endpoint, server_token=state.server_token, license=open(license_filename, 'r'))

    state.config.write_file()

    click.echo('Success')
