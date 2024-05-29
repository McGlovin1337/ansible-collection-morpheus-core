from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
name: search
author: James Riach (@McGlovin1337)
version_added: 0.x.x
short_description: Perform a Global Search of Morpheus
description:
    - Perform a general purpose global search of a Morpheus Appliance.
options:
    _terms:
        description:
            - The search terms to lookup.
    morpheus_host:
        description:
            - The Morpheus Hostname or IP Address to query.
        type: str
        env:
            - name: ANSIBLE_MORPHEUS_HOST
        vars:
            - name: ansible_morpheus_host
    morpheus_user:
        description:
            - The Username to connect to the Morpheus Appliance.
        type: str
        env:
            - name: ANSIBLE_MORPHEUS_USER
        vars:
            - name: ansible_morpheus_user
    morpheus_password:
        description:
            - The Password for the O(morpheus_user) to connect to the Morpheus Appliance.
        type: str
        env:
            - name: ANSIBLE_MORPHEUS_PASSWORD
        vars:
            - name: ansible_morpheus_password
    morpheus_token:
        description:
            - Specify an API Token instead of O(morpheus_user) or O(morpheus_password) parameters.
        type: str
        env:
            - name: ANSIBLE_MORPHEUS_TOKEN
        vars:
            - name: ansible_morpheus_token
    use_ssl:
        description:
            - Connect to Morpheus Appliance using an HTTPS/SSL Connection.
        type: bool
        default: True
    validate_certs:
        description:
            - Control whether to validate Morpheus Appliance SSL Certificates.
        type: bool
        default: True
notes:
    - When used with the 'morpheus.core.morpheus' httpapi plugin the O(morpheus_user), O(morpheus_password), and O(morpheus_token) parameters can be omitted
      with the value of O(morpheus_host) set to V(inventory_hostname).
'''

EXAMPLES = r'''
- name: Find items with the term "instance"
  ansible.builtin.debug:
    msg: "{{ q('morpheus.core.search', 'instance', morpheus_token='abcd...', morpheus_instance='cmp.domain.tld') }}"

- name: Search current Morpheus Appliance when used with httpapi plugin
  ansible.builtin.debug:
    msg: "{{ q('morpheus.core.search', 'instance', morpheus_instance=inventory_hostname) }}"
'''

RETURN = r'''
_list:
    description:
        - A list of matching items.
    type: list
    elements: dict
'''
import json
import urllib.parse
from urllib.error import HTTPError, URLError

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.plugins.lookup import LookupBase

try:
    import module_utils.morpheus_funcs as mf
except ModuleNotFoundError:
    import ansible_collections.morpheus.core.plugins.module_utils.morpheus_funcs as mf


class LookupModule(LookupBase):
    def _build_url(self, path: str, params: list[tuple] = None):
        url_parts = list(urllib.parse.urlparse(path))
        if params is not None:
            url_parts[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(url_parts)

    def _login(self, url: str, validate_certs: bool, username: str, password: str) -> str:
        full_url = self._build_url(
            path=url,
            params=[
                ('client_id', 'morph-api'),
                ('grant_type', 'password'),
                ('scope', 'write')
            ]
        )

        if username is None or len(username) == 0:
            raise AnsibleError('A username is required to login to {0}'.format(full_url))

        if password is None or len(password) == 0:
            raise AnsibleError('A password is required to login to {0}'.format(full_url))

        data = urllib.parse.urlencode({
            'username': username,
            'password': password
        })

        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }

        response = None
        try:
            response = open_url(
                url=full_url,
                data=data,
                validate_certs=validate_certs,
                method='POST',
                headers=headers
            )
        except HTTPError as e:
            raise AnsibleError('Received HTTP error for {0} : {1}'.format(full_url, to_native(e)))
        except URLError as e:
            raise AnsibleError('Failed lookup url for {0} : {1}'.format(full_url, to_native(e)))
        except SSLValidationError as e:
            raise AnsibleError("Error validating the server's certificate for {0}: {1}".format(full_url, to_native(e)))
        except ConnectionError as e:
            raise AnsibleError('Error connecting to {0}: {1}'.format(full_url, to_native(e)))

        response_data = json.loads(to_text(response.read()))

        if 'access_token' not in response_data:
            raise AnsibleError('Failed to retrieve an access token for {0}'.format(full_url))

        return response_data['access_token']

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        use_ssl = self.get_option('use_ssl')
        url_prefix = 'https://' if use_ssl else 'http://'
        search_url = '{0}{1}/api/search'.format(url_prefix, self.get_option('morpheus_host'))
        login_url = '{0}{1}/oauth/token'.format(url_prefix, self.get_option('morpheus_host'))

        validate_certs = self.get_option('validate_certs') if use_ssl else False

        token = self.get_option('morpheus_token')

        if token is None or len(token) == 0:
            token = self._login(
                url=login_url,
                validate_certs=validate_certs,
                username=self.get_option('morpheus_user'),
                password=self.get_option('morpheus_password')
            )

        headers = {
            'accept': 'application/json',
            'authorization': 'Bearer {0}'.format(token)
        }

        return_list = []

        for term in terms:
            query_url = self._build_url(search_url, [('phrase', term)])
            try:
                response = open_url(
                    url=query_url,
                    validate_certs=validate_certs,
                    headers=headers,
                    method='GET'
                )
            except HTTPError as e:
                raise AnsibleError('Received HTTP error for {0} : {1}'.format(query_url, to_native(e)))
            except URLError as e:
                raise AnsibleError('Failed lookup url for {0} : {1}'.format(query_url, to_native(e)))
            except SSLValidationError as e:
                raise AnsibleError("Error validating the server's certificate for {0}: {1}".format(query_url, to_native(e)))
            except ConnectionError as e:
                raise AnsibleError('Error connecting to {0}: {1}'.format(query_url, to_native(e)))

            response_data = json.loads(to_text(response.read()))

            for hit in response_data['hits']:
                return_list.append(mf.dict_keys_to_snake_case(hit))

        return return_list
