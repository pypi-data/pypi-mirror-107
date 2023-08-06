# -*- coding: utf-8 -*-

import time
from urllib.parse import urljoin

import click
import requests

from ..core.exceptions import BadCredentialsException, RequestError
from ..helpers.structures import DotDict
from .auth import HTTPAPIAuth, HTTPCLIAuth, HTTPUserTokenAuth


class APIClient(object):

    def __init__(self, endpoint, server_token=None, api_token=None, user_token=None):
        self.endpoint = endpoint
        self.server_token = server_token
        self.api_token = api_token
        self.user_token = user_token
        self.session = requests.Session()

    @classmethod
    def make_from_state(cls, state):
        config = state.config
        endpoint = config.get('testbrain', 'endpoint')
        server_token = config.get('testbrain', 'server_token')
        api_token = config.get('testbrain', 'api_token')
        user_token = config.get('testbrain', 'user_token')
        client = cls(endpoint=endpoint, server_token=server_token, user_token=user_token, api_token=api_token)
        return client

    @staticmethod
    def register(state, email, password, is_signed=False):

        session = requests.Session()
        url = 'https://app.appsurify.com/api/account/signup/v2/'
        resp = session.post(url, data={'email': email, 'password': password})
        if resp.status_code not in [200, 201, ]:
            raise BadCredentialsException(message=resp.text)
        resp_dict = DotDict(resp.json())
        time.sleep(10)

        click.echo('* Fetching user information...')
        endpoint = 'https://' + resp_dict.hostname
        client = APIClient(endpoint=endpoint)

        user_data = DotDict({})
        retry = 5
        while retry > 0:
            user_response = client.request_user_login(email=email, password=password)
            if user_response.status_code in [200, 201]:
                user_data = DotDict(user_response.json())
                break
            else:
                time.sleep(20)
                retry -= 1

        if user_data.empty:
            raise RequestError(message='Some problem during request user login')

        client.user_token = user_data.key

        profile_data = DotDict({})
        retry = 5
        while retry > 0:
            profile_response = client.request_user_profile()
            if profile_response.status_code in [200, 201]:
                profile_data = DotDict(profile_response.json())
                break
            else:
                time.sleep(20)
                retry -= 1

        if profile_data.empty:
            raise RequestError(message='Some problem during request user profile')

        # client.api_token = profile_data.api_key

        click.echo('* Fetching license information...')
        license_data = DotDict({})
        retry = 3
        while retry > 0:
            license_resp = client.request_list_licenses()
            if license_resp.status_code in [200, 201]:
                license_data = DotDict(license_resp.json())
                break
            else:
                time.sleep(10)
                retry -= 1

        if license_data.empty:
            raise RequestError(message='Some problem during request licenses')

        license_default = DotDict(list(filter(lambda x: x['default'] is True, license_data.results))[0])

        license_content = b''
        retry = 3
        while retry > 0:
            license_download_resp = client.request_download_licenses(license_default.id)
            if license_download_resp.status_code in [200, 201, ]:
                license_content = license_download_resp.content
                break
            else:
                time.sleep(10)
                retry -= 1

        if not license_content:
            raise RequestError(message='Some problem during request download license')

        result = DotDict({
            'email': email,
            'password': password,
            'user_token': user_data.key,
            'api_token': profile_data.api_key,
            'username': profile_data.username,
            'id': profile_data.id,
            'license': license_content.decode(),
            'uuid': license_default.uuid
        })
        return result

    def update_from_state(self, state):
        config = state.config
        self.endpoint = config.get('testbrain', 'endpoint')
        self.server_token = config.get('testbrain', 'server_token')
        self.api_token = config.get('testbrain', 'api_token')
        self.user_token = config.get('testbrain', 'user_token')
        return self

    def request_validate_server_token(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/token/server/')
        resp = session.get(url, auth=HTTPCLIAuth(token=self.server_token))
        return resp

    def request_validate_user_token(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/token/user/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_validate_api_token(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/token/api/')
        resp = session.get(url, auth=HTTPAPIAuth(token=self.api_token))
        return resp

    def request_current_organization(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/organization/')
        if self.api_token:
            resp = session.get(url, auth=HTTPAPIAuth(token=self.api_token))
        else:
            resp = session.get(url, auth=HTTPCLIAuth(token=self.server_token))
        return resp

    def request_create_from_license(self, license):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/license/init/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'license_key': license,
        })
        return resp

    def request_create_organization(self, company_name, email, password):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/organization/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'company_name': company_name,
            'email': email,
            'password': password
        })
        return resp

    def request_user_login(self, email, password):
        session = self.session
        url = urljoin(self.endpoint, '/api/account/login/')
        resp = session.post(url, data={
            'email': email,
            'password': password
        })
        return resp

    def request_user_profile(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/account/profile/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_list_project(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/projects/?fields=id,name')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_create_project(self, project_name):
        session = self.session
        url = urljoin(self.endpoint, '/api/projects/')
        resp = session.post(url, auth=HTTPUserTokenAuth(token=self.user_token), data={
            'name': project_name,
            'is_public': False,
            'is_active': True
        })
        return resp

    def request_list_licenses(self):
        session = self.session
        url = urljoin(self.endpoint, '/api/licenses/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_download_licenses(self, pk):
        session = self.session
        url = urljoin(self.endpoint, f'/api/licenses/{pk}/download/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_create_script_repository(self, project_id):
        session = self.session
        url = urljoin(self.endpoint, '/api/ssh_v2/repository/')
        resp = session.post(url, auth=HTTPUserTokenAuth(token=self.user_token), data={
            'project': project_id
        })
        return resp

    def request_script_hook(self, project, event, data):
        session = self.session
        url = urljoin(self.endpoint, '/api/ssh_v2/hook/{}/'.format(project))
        headers = {"X-Git-Event": event, "Content-Type": "application/json"}
        resp = session.post(url, auth=HTTPAPIAuth(token=self.api_token), headers=headers, data=data)
        return resp

    def request_add_license(self, license):
        session = self.session
        url = urljoin(self.endpoint, '/api/cli/license/add/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'license_key': license,
        })
        return resp
