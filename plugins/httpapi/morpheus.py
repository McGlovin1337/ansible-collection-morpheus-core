from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
name: morpheus
author: James Riach (@McGlovin1337)
short_description: Httpapi Plugin for Morpheus
description:
  - Httpapi plugin to connect to and manage morpheus appliances through the morpheus api.
version_added: "0.3.0"
options:
    morpheus_api_token:
        description:
            - Specify an API token instead of O(morpheus_user) and O(morpheus_password).
        type: str
        env:
            - name: ANSIBLE_MORPHEUS_TOKEN
        vars:
            - name: ansible_morpheus_token
'''

from ansible.module_utils.basic import to_native, to_text
from ansible.errors import AnsibleConnectionFailure, AnsibleAuthenticationFailure, AnsibleError
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.urls import open_url, SSLValidationError
from urllib.error import HTTPError, URLError
import json
import re
import time
import urllib.parse

try:
    from urllib3 import encode_multipart_formdata
    from urllib3.fields import RequestField
except (ImportError, ModuleNotFoundError) as imp_exc:
    URLLIB3_IMPORT_ERROR = imp_exc
else:
    URLLIB3_IMPORT_ERROR = None

LOGIN_PATH = '/oauth/token'
WHOAMI_PATH = '/api/whoami'

BASE_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        if URLLIB3_IMPORT_ERROR:
            raise AnsibleError('urllib3 must be installed to use this httpapi plugin') from URLLIB3_IMPORT_ERROR

        super(HttpApi, self).__init__(connection)
        self.headers = BASE_HEADERS
        self.access_token = None
        self.refresh_token = None
        self.token_timeout = None
        self.__refresh = False

    def _build_url(self, path: str, params: list[tuple] = None):
        url_parts = list(urllib.parse.urlparse(path))
        if params is not None:
            url_parts[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(url_parts)

    def _test_connection(self):
        _ = self.send_request(path=WHOAMI_PATH)

    def handle_httperror(self, exc):
        # Handle 5xx errors
        err_5xx = r'^5\d{2}$'

        handled_error = re.search(err_5xx, str(exc.code))
        if handled_error:
            raise AnsibleConnectionFailure('Could not connect to {0}: {1}'.format(self.connection._url, exc.reason))

        # Handle 400 Error when Authenticating
        if exc.code == 400:
            exc_data = self._response_to_json(exc.read())
            if exc_data['error'] == 'invalid_grant':
                raise AnsibleAuthenticationFailure('Failed to authenticate: {0}'.format(exc_data['error_description']))

        if exc.code == 401:
            if self.connection._auth:
                self.connection._auth = None
                if not all([self.refresh_token, self.connection.get_option('remote_user'), self.connection.get_option('password')]):
                    exc_data = self._response_to_json(exc.read())
                    raise AnsibleAuthenticationFailure('Failed to authenticate: {0}'.format(exc_data['error_description']))

                if self.refresh_token is not None:
                    self.__refresh = True

                self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))
                return True
            else:
                exc_data = self._response_to_json(exc.read())
                raise AnsibleAuthenticationFailure('Failed to authenticate: {0}'.format(exc_data['error_description']))

        return False

    def login(self, username, password):
        if self.access_token is None and not self.__refresh:
            self.access_token = self.get_option('morpheus_api_token')

        if self.access_token is not None and not self.__refresh:
            self.connection._auth = {'Authorization': 'Bearer {0}'.format(self.access_token)}
            self._test_connection()
            return

        use_ssl = self.connection.get_option('use_ssl')
        url_prefix = 'https://' if use_ssl else 'http://'
        root_url = '{0}{1}'.format(url_prefix, self.connection.get_option('host'))
        url = '{0}{1}'.format(root_url, LOGIN_PATH)
        grant_type = 'refresh_token' if self.__refresh else 'password'

        url_path = self._build_url(
            path=url,
            params=[
                ('client_id', 'morph-api'),
                ('grant_type', grant_type),
                ('scope', 'write')
            ]
        )

        payload = urllib.parse.urlencode({
            'username': username,
            'password': password
        }) if not self.__refresh else urllib.parse.urlencode({
            'refresh_token': self.refresh_token
        })

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response_data = None
        try:
            response = open_url(
                url=url_path,
                data=payload,
                headers=headers,
                method='POST',
                use_proxy=self.connection.get_option('use_proxy'),
                validate_certs=self.connection.get_option('validate_certs'),
                http_agent=self.connection.get_option('http_agent'),
                ca_path=self.connection.get_option('ca_path')
            )

            response_data = json.loads(to_text(response.read()))
        except (HTTPError, URLError) as e:
            raise AnsibleError('Authentication Failure, received error for {0} : {1}'.format(url, to_native(e)))
        except SSLValidationError as e:
            raise AnsibleError("Error validating the server's certificate for {0}: {1}".format(url, to_native(e)))
        except ConnectionError as e:
            raise AnsibleError('Error connecting to {0}: {1}'.format(url, to_native(e)))

        if response_data is not None:
            try:
                self.access_token = response_data['access_token']
                self.refresh_token = response_data['refresh_token']
                self.token_timeout = int(time.time()) + int(response_data['expires_in'])
                self.connection._auth = {'Authorization': 'Bearer {0}'.format(response_data['access_token'])}
                self.__refresh = False
            except KeyError:
                raise AnsibleAuthenticationFailure('Failed to retrieve an access_token: %s' % response_data)

        self._test_connection()

    def update_auth(self, response, response_text):
        """Ignore the response params, this method ensures a token is set"""

        # If we know the token expiry and the expiry is within the next hour
        # use the refresh_token to acquire a new token
        if self.token_timeout is not None\
            and self.token_timeout - int(time.time()) < 3600\
                and self.refresh_token is not None:
            self.connection._auth = None
            self.__refresh = True
            self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))

        if self.access_token:
            self.connection._auth = {'Authorization': 'Bearer {0}'.format(self.access_token)}

    def send_request(self, data=None, **kwargs) -> dict:
        if self.connection._auth is None:
            self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))

        path = kwargs.pop('path', None)
        method = kwargs.pop('method', 'GET')
        headers = kwargs.pop('headers', self.headers)

        if headers['Content-Type'].split(';')[0] not in ['application/x-www-form-urlencoded', 'application/octet-stream', 'multipart/form-data']:
            data = json.dumps(data) if data is not None else None

        try:
            response, response_data = self.connection.send(path, data, method=method, headers=headers, **kwargs)
        except HTTPError as exc:
            try:
                exc_data = self._response_to_json(exc.read())
            except ConnectionError:
                exc_data = exc.read()

            return dict(code=exc.code, contents=exc_data, path=path)

        response_value = self._get_response_value(response_data)
        return dict(code=response.getcode(), contents=self._response_to_json(response_value))

    def multipart_upload(self, uri_path: str, file_data: list[dict]) -> dict:
        """Takes a list of files for multipart/form-data file uploads.

        Args:
            uri_path (str): Send request to this path.
            file_data (list[dict]): List of dictionaries containing files to upload.
             The dictionary should be in the format of {'name': 'name for the body param', 'file_path': 'path/to/file'}

        Returns:
            dict: Dictionary containing response code and any returned data.
        """
        request_fields = []
        for item in file_data:
            with open(item['file_path'], 'rb') as file_item:
                rf = RequestField(
                    name=item['name'],
                    data=file_item.read(),
                    filename=file_item.name.split('/')[-1])
                rf.make_multipart()
                request_fields.append(rf)

        body, content_type = encode_multipart_formdata(request_fields)
        headers = self.headers.copy()
        headers['Content-Type'] = content_type
        headers['Content-Length'] = len(body)

        try:
            response, response_data = self.connection.send(uri_path, body, method='POST', headers=headers)
        except HTTPError as exc:
            try:
                exc_data = self._response_to_json(exc.read())
            except ConnectionError:
                exc_data = exc.read()

            return dict(code=exc.code, contents=exc_data, path=uri_path)

        response_value = self._get_response_value(response_data)
        contents = self._response_to_json(response_value)
        return dict(code=response.getcode(), contents=contents)

    def _get_response_value(self, response_data):
        return to_text(response_data.getvalue())

    def _response_to_json(self, response_text):
        try:
            return json.loads(response_text) if response_text else {}
        except ValueError:
            raise ConnectionError('Invalid JSON response: %s' % response_text)
