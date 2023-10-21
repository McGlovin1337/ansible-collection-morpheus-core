#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: virtual_image
short_description: Manage Morpheus Virtual Images
description:
    - Manage Morpheus Virtual Images.
version_added: 0.x.x
author: James Riach
options:
    state:
        description:
            - Create, update or remove a Virtual Image.
            - If I(state=absent) and I(filename) is specified then remove the specified file.
        default: present
        choices:
            - absent
            - present
        type: string
    virtual_image_id:
        description:
            - Specify Virtual Image by Id.
        type: int
    name:
        description:
            - Set the Name of the Virtual Image
        type: string
    filename:
        description:
            - Name of uploaded file.
        type: string
    file_path:
        description:
            - Path to local file to upload.
        type: string
    file_url:
        description:
            - URL of file to upload.
        type: string
    labels:
        description:
            - Provide a list of labels to apply to Virtual Image.
        type: list
        elements: string
    image_type:
        description:
            - Set the Image Type code, e.g. vmware
        type: string
    storage_provider_id:
        description:
            - Specify the Storage Provider by Id.
        type: int
    is_cloud_init:
        description:
            - Specify if Cloud Init is enabled.
        type: bool
    user_data:
        description:
            - Cloud Init user data.
        type: string
    install_agent:
        description:
            - Specify if Morpheus Agent should be installed.
        type: bool
    username:
        description:
            - Specify the Username for the Virtual Image.
        type: string
    password:
        description:
            - Specify the Password for the Virtual Image.
        type: string
    ssh_key:
        description:
            - Specify an SSH Key for the Virtual Image.
        type: string
    os_type:
        description:
            - Specify the OS Type code or name.
        type: string
    visibility:
        description:
            - If the Virtual Image should be private or public.
        choices:
            - private
            - public
        type: string
    accounts:
        description:
            - List of Tenants by Id Virtual Image is available to.
        type: list
        elements: int
    is_auto_join_domain:
        description:
            - Whether to Auto Join Domain.
        type: bool
    virtio_supported:
        description:
            - Are Virtio Drivers installed.
        type: bool
    vm_tools_installed:
        description:
            - Are VMware Tools installed.
        type: bool
    trial_version:
        description:
            - Is the Virtual Image a Trial Version.
        default: false
        type: bool
    is_sysprep:
        description:
            - Specify if Sysprep is Enabled.
        type: bool
    azure_config:
        description:
            - For Azure Virtual Images, specify further options.
        type: dict
        suboptions:
            publisher:
                description:
                    - Name of Publisher in the Azure Marketplace.
                type: string
            offer:
                description:
                    - Name of Offer in the Azure Marketplace.
                type: string
            sku:
                description:
                    - Name of SKU in the Azure Marketplace.
                type: string
            version:
                description:
                    - Name of Version in the Azure Marketplace.
                type: string
    config:
        description:
            - Dictionary of Virtual Image configuration.
        type: dict
    tags:
        description:
            - List of Tags to apply.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The Tag name.
                type: string
            value:
                description:
                    - The Tag value.
                type: string
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

from copy import deepcopy
from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

try:
    import module_utils.morpheus_funcs as mf
    from module_utils.morpheusapi import MorpheusApi
except ModuleNotFoundError:
    import ansible_collections.morpheus.core.plugins.module_utils.morpheus_funcs as mf
    from ansible_collections.morpheus.core.plugins.module_utils.morpheusapi import MorpheusApi


def create_update_vi(module: AnsibleModule, morpheus_api: MorpheusApi) -> dict:
    vi_response = {}
    upload_response = False
    diffs = []

    virtual_image = get_vi(module.params, morpheus_api)

    if len(virtual_image) > 1:
        module.fail_json(
            msg='Number of matching Virtual Images exceeded 1, got {0}'.format(len(virtual_image))
        )

    api_params, file_params = module_to_api_params(module.params)

    try:
        api_params['virtual_image_id'] = virtual_image[0]['id']
    except (KeyError, IndexError):
        api_params['virtual_image_id'] = None
        virtual_image = []

    action = {
        0: partial(morpheus_api.create_virtual_image, api_params=api_params),
        1: partial(morpheus_api.update_virtual_image, api_params=api_params),
        3: partial(parse_check_mode, state=module.params['state'], api_params=api_params, virtual_images=virtual_image)
    }.get(len(virtual_image) if not module.check_mode else 3)

    vi_action = action()
    vi_response = mf.dict_keys_to_snake_case(vi_action)

    try:
        vi_id = vi_response['id']
        if module._diff:
            vi_changed, diff = mf.dict_diff(vi_response, virtual_image[0], {'last_updated'})
            diffs.append({
                'after_header': '{0} ({1})'.format(vi_response['name'], vi_response['id']),
                'after': '\n'.join([d['after'] for d in diff]),
                'before_header': '{0}, ({1})'.format(virtual_image[0]['name'], virtual_image[0]['id']),
                'before': '\n'.join([d['before'] for d in diff])
            })
        else:
            vi_changed = not mf.dict_compare_equality(virtual_image[0], vi_response, {'last_updated'})
    except KeyError:
        vi_id = None
        vi_changed = False
    except IndexError:
        vi_changed = True
        if module._diff:
            diffs.append({
                'after_header': '{0} ({1})'.format(vi_response['name'], vi_response['id']),
                'after': 'Created Virtual Image\n',
                'before_header': '{0}, ({1})'.format(vi_response['name'], vi_response['id']),
                'before': 'Non-Existent Virtual Image\n'
            })

    if file_params['filename'] is not None and vi_id is not None:
        file_params['virtual_image_id'] = vi_id
        upload_action = {
            'False': partial(morpheus_api.upload_virtual_image_file, api_params=file_params),
            'True': partial(parse_check_mode, state=module.params['state'], file_params=file_params, virtual_images=virtual_image)
        }.get(module.check_mode)
        exec_upload_action = upload_action()
        upload_response = mf.success_response(exec_upload_action)[0]

    result = {
        'changed': vi_changed is True or upload_response is True,
        'virtual_image': vi_response
    }

    if module._diff:
        result['diff'] = diffs

    return result


def get_vi(module_params: dict, morpheus_api: MorpheusApi) -> list:
    virtual_image = []

    api_params, _ = module_to_api_params(module_params)

    if module_params['virtual_image_id'] is not None:
        virtual_image = [morpheus_api.get_virtual_images(api_params)]
        try:
            _ = virtual_image[0]['id']
        except KeyError:
            virtual_image = []

    if module_params['name'] is not None and len(virtual_image) == 0:
        virtual_image = morpheus_api.get_virtual_images({'virtual_image_id': None, 'name': api_params['name']})

    virtual_image = [mf.dict_keys_to_snake_case(vi) for vi in virtual_image]

    return virtual_image


def module_to_api_params(module_params: dict) -> tuple:
    api_params = module_params.copy()

    api_params['ssh_username'] = api_params.pop('username')
    api_params['ssh_password'] = api_params.pop('password')
    if api_params['azure_config'] is not None:
        if api_params['config'] is None:
            api_params['config'] = {}
        api_params['config'].update(api_params.pop('azure_config'))
    del api_params['state']

    file_params = {
        'virtual_image_id': api_params['virtual_image_id'] if api_params['virtual_image_id'] is not None else 0,
        'filename': api_params.pop('filename'),
        'file': api_params.pop('file_path'),
        'url': api_params.pop('file_url')
    }

    return api_params, file_params


def parse_check_mode(state: str, virtual_images: list, api_params: dict = None, file_params: dict = None):
    images = deepcopy(virtual_images)

    if state == 'absent':
        try:
            _ = images[0]['id']
        except (IndexError, KeyError):
            return {
                'success': False,
                'msg': 'Virtual Image not found'
            }

        return {'success': True}

    if api_params is not None:
        try:
            api_params['id'] = api_params.pop('virtual_image_id')
        except KeyError:
            pass

        try:
            api_params['accounts'] = [{'id': aid} for aid in api_params['accounts']]
        except KeyError:
            pass

        try:
            api_params['config'].update(api_params.pop('azure_config'))
        except (AttributeError, KeyError):
            try:
                api_params['config'] = api_params.pop('azure_config')
            except KeyError:
                pass

        virtual_image = {}
        try:
            virtual_image = images[0]
            for k, v in api_params.items():
                if v is not None:
                    virtual_image[k] = v
        except IndexError:
            virtual_image = api_params
        except KeyError:
            pass

        try:
            _ = virtual_image['id']
        except KeyError:
            virtual_image['id'] = -1

        return virtual_image

    if file_params is not None:
        try:
            _ = images[0]['id']
        except (IndexError, KeyError):
            return {
                'success': False,
                'msg': 'Virtual Image not found'
            }

        return {
            'success': True,
        }


def remove_vi(module: AnsibleModule, morpheus_api: MorpheusApi) -> dict:
    virtual_image = get_vi(module.params, morpheus_api)

    if len(virtual_image) > 1:
        module.fail_json(
            msg='Number of matching Virtual Images exceeded 1, got {0}'.format(len(virtual_image))
        )

    try:
        _ = virtual_image[0]['id']
    except (IndexError, KeyError):
        module.fail_json(
            msg='No Virtual Images matched query parameters'
        )

    _, file_params = module_to_api_params(module.params)
    file_params['virtual_image_id'] = virtual_image[0]['id']

    action = {
        0: partial(morpheus_api.delete_virtual_image, virtual_image[0]['id']),
        1: partial(morpheus_api.delete_virtual_image_file, file_params),
        2: partial(parse_check_mode, state=module.params['state'], virtual_images=virtual_image)
    }.get(int(module.params['filename'] is None) if not module.check_mode else 2)

    response = action()

    success, msg = mf.success_response(response)

    result = {
        'changed': success,
        'msg': msg
    }

    if module._diff:
        prepared_action = 'Remove file {0} from Virtual Image \'{1}\'\n'.format(module.params['filename'], virtual_image[0]['name']) \
            if module.params['filename'] is not None \
            else 'Remove Virtual Image \'{0}\' ({1})\n'.format(virtual_image[0]['name'], virtual_image[0]['id'])
        result['diff'] = [{
            'prepared': prepared_action
        }]

    return result


def run_module():
    argument_spec = {
        'state': {'type': 'str', 'choices': ['absent', 'present'], 'default': 'present'},
        'virtual_image_id': {'type': 'int'},
        'name': {'type': 'str'},
        'filename': {'type': 'str'},
        'file_path': {'type': 'str'},
        'file_url': {'type': 'str'},
        'labels': {'type': 'list', 'elements': 'str'},
        'image_type': {'type': 'str'},
        'storage_provider_id': {'type': 'int'},
        'is_cloud_init': {'type': 'bool'},
        'user_data': {'type': 'str'},
        'install_agent': {'type': 'bool'},
        'username': {'type': 'str'},
        'password': {'type': 'str', 'no_log': 'true'},
        'ssh_key': {'type': 'str', 'no_log': 'true'},
        'os_type': {'type': 'str'},
        'visibility': {'type': 'str', 'choices': ['private', 'public']},
        'accounts': {'type': 'list', 'elements': 'int'},
        'is_auto_join_domain': {'type': 'bool'},
        'virtio_supported': {'type': 'bool'},
        'vm_tools_installed': {'type': 'bool'},
        'trial_version': {'type': 'bool'},
        'is_sysprep': {'type': 'bool'},
        'azure_config': {
            'type': 'dict',
            'options': {
                'publisher': {'type': 'str'},
                'offer': {'type': 'str'},
                'sku': {'type': 'str'},
                'version': {'type': 'str'}
            }
        },
        'config': {'type': 'dict'},
        'tags': {
            'type': 'list',
            'elements': 'dict',
            'options': {
                'name': {'type': 'str'},
                'value': {'type': 'str'}
            }
        }
    }

    result = {
        'changed': False,
        'virtual_image': {}
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    connection = Connection(module._socket_path)
    morpheus_api = MorpheusApi(connection)

    action = {
        'absent': remove_vi,
        'present': create_update_vi
    }.get(module.params['state'])

    action_result = action(module, morpheus_api)

    result.update(action_result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()