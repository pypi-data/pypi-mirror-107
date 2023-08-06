# -*- coding: utf-8 -*-

import base64
from urllib.parse import urlparse, urlunparse

import click

from ..core.state import State


class URL(click.ParamType):
    name = 'url'

    def convert(self, value, param, ctx):
        if not isinstance(value, tuple):
            value = urlparse(value)
            if value.scheme not in ('http', 'https') or not value.netloc:
                self.fail(
                    '',
                    param,
                    ctx,
                )
        return urlunparse(value)


class ServerToken(click.ParamType):
    name = 'server-token'

    def convert(self, value, param, ctx):
        return base64.b64encode(value.encode()).decode()
