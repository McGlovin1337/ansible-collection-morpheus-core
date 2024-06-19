#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: environment_info
short_description: Retrieves Environments
description:
    - Retrieves information about configured environments.
version_added: 0.x.x
author: James Riach (@McGlovin1337)
options:
    code:
        description:
            - Match by the environment code attribute.
        type: str
extends_documentation_fragment:
    - morpheus.core.generic_name_filter
    - action_common_attributes
attributes:
    check_mode:
        support: none
    diff_mode:
        support: none
    platform:
        platforms:
            - httpapi
'''

EXAMPLES = r'''
- name: Retrieve all Environments
  morpheus.core.environment_info:

- name: Retrieve dev & test Environments using Regex
  morpheus.core.environment_info:
    name: ^(dev|test).*$
    regex_match: true
'''

RETURN = r'''
environments:
    description:
        - A List of matching Environments.
    type: list
    sample:
        "environments": [
            {
                "account": null,
                "active": true,
                "code": "dev",
                "date_created": "2024-01-01T00:00:01Z",
                "description": "Development",
                "id": 1,
                "last_updated": "2024-01-01T00:00:01Z",
                "name": "Dev",
                "sort_order": 1,
                "visibility": "private"
            }
        ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
try:
    import module_utils._info_module_common as info_module
    import module_utils.morpheus_funcs as mf
    from module_utils.morpheusapi import ApiPath, MorpheusApi
except ModuleNotFoundError:
    import ansible_collections.morpheus.core.plugins.module_utils._info_module_common as info_module
    import ansible_collections.morpheus.core.plugins.module_utils.morpheus_funcs as mf
    from ansible_collections.morpheus.core.plugins.module_utils.morpheusapi import ApiPath, MorpheusApi


def run_module():
    argument_spec = {
        **info_module.COMMON_ARG_SPEC,
        **{
            'code': {'type': 'str'}
        }
    }

    result = {
        'changed': False,
        'environments': []
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=info_module.COMMON_MUTUALLY_EXCLUSIVE,
        supports_check_mode=False
    )

    connection = Connection(module._socket_path)
    morpheus_api = MorpheusApi(connection)

    api_params = info_module.param_filter(module)

    response = morpheus_api.common_get(ApiPath.ENVIRONMENTS_PATH, api_params)

    response = info_module.response_filter(module, response)

    result['environments'] = [mf.dict_keys_to_snake_case(response_item) for response_item in response]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
