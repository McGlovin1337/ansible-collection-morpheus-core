#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: environment
short_description: Manage Environments
description:
    - Create, Update and Remove Environments.
version_added: 0.x.x
author: James Riach (@McGlovin1337)
options:
    state:
        description:
            - V(present) will create or update an Environment, or V(absent) will remove an Environment.
        choices:
            - absent
            - present
        default: present
        type: str
    id:
        description:
            - Id of an existing Environment.
        type: int
    name:
        description:
            - Name of the Environment.
        type: str
    code:
        description:
            - Short Code name for the Environment.
            - Note, that this is only applicable when creating a new Environment.
        type: str
    visibility:
        description:
            - Whether the Environment is Public or Private.
        choices:
            - private
            - public
        type: str
    sort_order:
        description:
            - The order in which Environments are presented.
        type: int
    active:
        description:
            - Set the Active state of the Environment.
        type: bool
extends_documentation_fragment:
    - action_common_attributes
attributes:
    check_mode:
        support: full
    diff_mode:
        support: full
    platform:
        platforms:
            - httpapi
'''

EXAMPLES = r'''
- name: Create/Update Environment
  morpheus.core.environment:
    state: present
    name: Development Environment
    code: dev
    sort_order: 0
    active: true
    visibility: private

- name: Remove Environment
  morpheus.core.environment:
    state: absent
    name: Development Environment
'''

RETURN = r'''
environment:
    description:
        - Environment Information.
    type: dict
    returned: always
    sample:
        "environment": {
            "account": {
                "id": 1,
                "name": "Tenant"
            },
            "active": true,
            "code": "dev",
            "date_created": "2024-01-01T00:00:01Z",
            "description": null,
            "id": 50,
            "last_updated": "2024-01-01T00:00:01Z",
            "name": "Development Environment",
            "sort_order": 0,
            "visibility": "private"
        }
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
try:
    import module_utils.morpheus_funcs as mf
    from module_utils.morpheusapi import ApiPath, MorpheusApi
except ModuleNotFoundError:
    import ansible_collections.morpheus.core.plugins.module_utils.morpheus_funcs as mf
    from ansible_collections.morpheus.core.plugins.module_utils.morpheusapi import ApiPath, MorpheusApi


MOCK_ENVIRONMENT = {
    "id": 0,
    "account": {
      "id": 0,
      "name": "Known After Create"
    },
    "code": "Known After Create",
    "name": "Known After Create",
    "description": "Known After Create",
    "visibility": "private",
    "active": True,
    "sortOrder": 0,
    "dateCreated": "",
    "lastUpdated": ""
}


def create_update_environment(module: AnsibleModule, morpheus_api: MorpheusApi, existing_env: dict) -> dict:
    """Create a new Environment or Update an existing one.

    Args:
        module (AnsibleModule): An instantiated AnsibleModule Class
        morpheus_api (MorpheusApi): An instantiated MorpheusApi Class
        existing_env (dict): Details of an existing Group

    Returns:
        dict: Result of the creation or update request
    """
    api_params = module_to_api_params(module.params)

    if 'id' in existing_env and api_params['id'] is None:
        api_params['id'] = existing_env['id']

    action = {
        'False': partial(morpheus_api.common_create, path=ApiPath.ENVIRONMENTS_PATH, api_params=api_params),
        'True': partial(morpheus_api.common_set, path=ApiPath.ENVIRONMENTS_PATH, item_id=api_params.pop('id'), api_params=api_params),
        'Check': partial(parse_check_mode, state=module.params['state'], api_params=api_params, existing_env=existing_env)
    }.get(str('id' in existing_env) if not module.check_mode else 'Check')

    action_result = action()
    action_result = mf.dict_keys_to_snake_case(action_result)

    changed, diff = mf.dict_diff(action_result, existing_env, {'last_updated', })
    result = {
        'changed': changed and 'id' in action_result,
        'environment': action_result
    }

    if module._diff:
        diffs = []

        if result['changed']:
            if 'id' in existing_env:
                diffs.append({
                    'after_header': '{0} ({1})'.format(action_result['name'], action_result['id']),
                    'after': '\n'.join([d['after'] for d in diff]),
                    'before_header': '{0} ({1})'.format(existing_env['name'], existing_env['id']),
                    'before': '\n'.join([d['before'] for d in diff])
                })
            else:
                diffs.append({
                    'after_header': '{0} ({1})'.format(action_result['name'], action_result['id']),
                    'after': 'Create new Environment\n',
                    'before_header': 'Non-existent Environment',
                    'before': 'Non-existent Environment\n'
                })

        result['diff'] = diffs

    return result


def get_existing_environment(module: AnsibleModule, morpheus_api: MorpheusApi) -> dict:
    """Returns an existing environment if one matches the module parameters.

    Args:
        module (AnsibleModule): An instantiated AnsibleModule Class
        morpheus_api (MorpheusApi): An instantiated MorpheusApi Class

    Returns:
        dict: Dictionary details of the existing environment if it exists
    """
    existing_env = morpheus_api.common_get(
        ApiPath.ENVIRONMENTS_PATH,
        {
            'id': module.params['id'],
            'name': module.params['name']
        }
    )

    if isinstance(existing_env, list):
        if len(existing_env) > 1:
            module.fail_json(
                msg='Number of matching environments exceeded 1, got {0}'.format(len(existing_env))
            )
        existing_env = existing_env[0] if len(existing_env) == 1 else {}

    return mf.dict_keys_to_snake_case(existing_env)


def module_to_api_params(module_params: dict) -> dict:
    """Convert Module Parameters to API Parameters.

    Args:
        module_params (dict): Ansible Module Parameters

    Returns:
        dict: Dictionary of API Parameters
    """
    api_params = module_params.copy()

    del api_params['state']

    return api_params


def parse_check_mode(state: str, api_params: dict, existing_env: dict) -> dict:
    """Returns a predicted result when the module is run in check mode.

    Args:
        state (str): The value of the module state parameter
        api_params (dict): API Parameters
        existing_env (dict): Details of an existing group if it exists

    Returns:
        dict: Predicted result
    """
    if state == 'absent':
        return {'success': True, 'msg': ''}

    updated_env = existing_env.copy() if len(existing_env) > 0 else MOCK_ENVIRONMENT

    if 'id' not in existing_env:
        existing_env = MOCK_ENVIRONMENT
    else:
        del api_params['code']  # The API Update Method doesn't allow changing code, so we mock that

    for k, v in api_params.items():
        updated_env[k] = v

    return updated_env


def remove_environment(module: AnsibleModule, morpheus_api: MorpheusApi, existing_env: dict) -> dict:
    """Removes an existing environment.

    Args:
        module (AnsibleModule): An instantiated AnsibleModule Class
        morpheus_api (MorpheusApi): An instantiated MorpheusApi Class
        existing_env (dict): Dictionary details of an existing environment

    Returns:
        dict: Result dictionary
    """
    if 'id' not in existing_env:
        module.fail_json(
            msg='Specified Environment does not exist'
        )

    action = {
        'False': partial(morpheus_api.common_delete, path=ApiPath.ENVIRONMENTS_PATH, item_id=existing_env['id']),
        'True': partial(parse_check_mode, state='absent', api_params={}, existing_env=existing_env)
    }.get(str(module.check_mode))

    response = action()
    success, msg = mf.success_response(response)

    return {
        'changed': success,
        'failed': not success,
        'msg': msg
    }


def run_module():
    argument_spec = {
        'state': {'type': 'str', 'choices': ['absent', 'present'], 'default': 'present'},
        'id': {'type': 'int'},
        'name': {'type': 'str'},
        'code': {'type': 'str'},
        'visibility': {'type': 'str', 'choices': ['private', 'public']},
        'sort_order': {'type': 'int'},
        'active': {'type': 'bool'}
    }

    result = {
        'changed': False,
        'environment': {}
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    connection = Connection(module._socket_path)
    morpheus_api = MorpheusApi(connection)

    existing_environment = get_existing_environment(module, morpheus_api)

    action = {
        'absent': remove_environment,
        'present': create_update_environment
    }.get(module.params['state'])

    action_result = action(module=module, morpheus_api=morpheus_api, existing_env=existing_environment)

    result.update(action_result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
