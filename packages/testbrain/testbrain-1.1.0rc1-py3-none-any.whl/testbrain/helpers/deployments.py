# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
from urllib.parse import urljoin

import click

from ..client.client import APIClient
from ..core.exceptions import HookExistsError, HookSetupError


def prepare_docker_compose_env(state, directory, reinstall=False):

    testbrain_dir = Path(__file__).parent.parent.resolve()
    template_file_path = Path.joinpath(testbrain_dir, 'templates', 'docker-compose.yml-tpl')
    template = open(template_file_path, 'r').read()
    template = template.replace("{{DEPLOYMENT_DIR}}", str(directory))

    directory = Path(directory).resolve()
    directory.mkdir(mode=0o777, parents=True, exist_ok=True)

    paths = [
        'var',
        'log',
        'storage',
        'media',
        'static',
        'secret',
        'run',
        'var/lib/postgresql/data',
        'var/lib/rabbitmq',
        'log/nginx',
        'log/gunicorn',
    ]

    for path in paths:
        Path(Path.joinpath(directory, path)).mkdir(mode=0o777, parents=True, exist_ok=True)

    docker_compose_file_name = 'docker-compose.yml'
    docker_compose_file = open(Path.joinpath(directory, docker_compose_file_name), 'w+')
    docker_compose_file.write(template)
    docker_compose_file.flush()
    docker_compose_file.close()

    return True
