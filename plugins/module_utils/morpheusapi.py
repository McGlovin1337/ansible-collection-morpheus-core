from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
name: morpheusapi
short_description: Morpheus Api Helper Class
description:
    - Ansible Module Utility for interfacing with the Morpheus API
version_added: 0.3.0
author: James Riach
'''

import urllib.parse
try:
    import morpheus_funcs as mf
except ModuleNotFoundError:
    import ansible_collections.morpheus.core.plugins.module_utils.morpheus_funcs as mf


APPLIANCE_SETTINGS_PATH = '/api/appliance-settings'
CLOUDS = '/api/zones'
CLOUD_DATASTORES = '/api/zones/{0}/data-stores'
CLOUD_TYPES = '/api/zone-types'
GROUPS_PATH = '/api/groups'
HEALTH_PATH = '/api/health'
INSTANCES_PATH = '/api/instances'
INTEGRATIONS_PATH = '/api/integrations'
KEY_PAIR_PATH = '/api/key-pairs'
LICENSE_PATH = '/api/license'
MAINTENANCE_MODE_PATH = '{}/maintenance'.format(APPLIANCE_SETTINGS_PATH)
ROLES_PATH = '/api/roles'
SNAPSHOTS_PATH = '/api/snapshots'
SSL_CERTIFICATES_PATH = '/api/certificates'
TENANTS_PATH = '/api/accounts'
VIRTUAL_IMAGES_PATH = '/api/virtual-images'


class MorpheusApi():
    def __init__(self, connection) -> None:
        self.connection = connection

    def _build_url(self, path: str, params: list[tuple] = None):
        url_parts = list(urllib.parse.urlparse(path))
        if params is not None:
            url_parts[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(url_parts)

    def _get_object(self, api_path: str, api_params: dict, max_param: bool = False):
        params = mf.dict_keys_to_camel_case(api_params)
        if max_param:
            params['max'] = -1
        url_params = self._url_params(params)
        path = self._build_url(api_path, url_params)

        return self.connection.send_request(path=path)

    def _get_object_by_id(self, api_path: str, obj_id: int, url_params: dict = None):
        path = '{0}/{1}'.format(api_path, obj_id)

        if url_params is not None:
            url_params = self._url_params(url_params)
            path = self._build_url(path, url_params)

        return self.connection.send_request(path=path)

    def _payload_from_params(self, params: dict):
        payload = mf.dict_keys_to_camel_case(
            {k: v for k, v in params.items() if v is not None}
        )

        return payload

    def _return_reponse_key(self, response: dict, key: str):
        if key is None or key == '':
            try:
                return response['contents']
            except KeyError:
                return response

        try:
            return response['contents'][key]
        except KeyError:
            try:
                return response['contents']
            except KeyError:
                return response

    def _url_params(self, params: dict):
        args = []

        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, list):
                for item in v:
                    args.append((k, item))
                continue
            if isinstance(v, bool):
                v = str(v).lower()
            args.append((k, v))

        return args

    def backup_instance(self, instance_id: int):
        path = '{0}/{1}/backup'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def create_cloud(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'zone': payload}

        response = self.connection.send_request(
            data=body,
            path=CLOUDS,
            method='POST'
        )
        return self._return_reponse_key(response, 'zone')

    def create_group(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'group': payload}

        response = self.connection.send_request(
            data=body,
            path=GROUPS_PATH,
            method='POST'
        )
        return self._return_reponse_key(response, 'group')

    def create_key_pair(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'keyPair': payload}

        path = KEY_PAIR_PATH

        if len(body['keyPair']) == 1 and bool(api_params['name']):
            path = '{0}/generate'.format(KEY_PAIR_PATH)

        response = self.connection.send_request(
            data=body,
            path=path,
            method='POST'
        )
        return self._return_reponse_key(response, '')

    def create_ssl_certificate(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'certificate': payload}

        response = self.connection.send_request(
            data=body,
            path=SSL_CERTIFICATES_PATH,
            method='POST'
        )
        return self._return_reponse_key(response, 'certificate')

    def create_virtual_image(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'virtualImage': payload}

        response = self.connection.send_request(
            data=body,
            path=VIRTUAL_IMAGES_PATH,
            method='POST'
        )
        return self._return_reponse_key(response, 'virtualImage')

    def delete_all_instance_snapshots(self, instance_id: int):
        path = '{0}/{1}/delete-all-snapshots'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_cloud(self, cloud_id: int, api_params: dict):
        path = '{0}/{1}'.format(CLOUDS, cloud_id)
        params = mf.dict_keys_to_camel_case(api_params)
        url_params = self._url_params(params)
        path = self._build_url(path, url_params)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_group(self, group_id: int):
        path = '{0}/{1}'.format(GROUPS_PATH, group_id)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_instance(self, instance_id: int, api_params: dict):
        path = '{0}/{1}'.format(INSTANCES_PATH, instance_id)
        params = mf.dict_keys_to_camel_case(api_params)
        url_params = self._url_params(params)
        path = self._build_url(path, url_params)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, 'results')

    def delete_key_pair(self, key_pair_id: int):
        path = '{0}/{1}'.format(KEY_PAIR_PATH, key_pair_id)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_snapshot(self, snapshot_id: int):
        path = '{0}/{1}'.format(SNAPSHOTS_PATH, snapshot_id)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_ssl_certificate(self, cert_id: int):
        path = '{0}/{1}'.format(SSL_CERTIFICATES_PATH, cert_id)
        response = self.connection.send_request(path=path, method='DELETE')
        return self._return_reponse_key(response, '')

    def delete_virtual_image(self, virtual_image_id: int):
        path = '{0}/{1}'.format(VIRTUAL_IMAGES_PATH, virtual_image_id)

        response = self.connection.send_request(path=path, method='DELETE')

        return self._return_reponse_key(response, '')

    def delete_virtual_image_file(self, api_params: dict):
        path = '{0}/{1}/files'.format(VIRTUAL_IMAGES_PATH, api_params['virtual_image_id'])

        url_params = self._url_params({'filename': api_params['filename']})
        path = self._build_url(path, url_params)

        response = self.connection.send_request(path=path, method='DELETE')

        return self._return_reponse_key(response, '')

    def eject_instance(self, instance_id: int):
        path = '{0}/{1}/eject'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def get_appliance_health(self):
        response = self.connection.send_request(path=HEALTH_PATH)
        return self._return_reponse_key(response, 'health')

    def get_appliance_license(self):
        response = self.connection.send_request(path=LICENSE_PATH)
        return self._return_reponse_key(response, 'license')

    def get_appliance_settings(self):
        response = self.connection.send_request(path=APPLIANCE_SETTINGS_PATH)
        return self._return_reponse_key(response, 'applianceSettings')

    def get_clouds(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(CLOUDS, api_params['id'])
            return self._return_reponse_key(response, 'zone')

        response = self._get_object(CLOUDS, api_params, True)
        return self._return_reponse_key(response, 'zones')

    def get_cloud_datastores(self, api_params: dict):
        zone_id = api_params.pop('zone_id')

        if api_params['id'] is not None:
            response = self._get_object_by_id(CLOUD_DATASTORES.format(zone_id), api_params['id'])
            return self._return_reponse_key(response, 'datastore')

        response = self._get_object(CLOUD_DATASTORES.format(zone_id), api_params, True)
        return self._return_reponse_key(response, 'datastores')

    def get_cloud_types(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(CLOUD_TYPES, api_params['id'])
            return self._return_reponse_key(response, 'zoneType')

        response = self._get_object(CLOUD_TYPES, api_params, True)
        return self._return_reponse_key(response, 'zoneTypes')

    def get_groups(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(GROUPS_PATH, api_params['id'])
            return self._return_reponse_key(response, 'group')

        response = self._get_object(GROUPS_PATH, api_params, True)
        return self._return_reponse_key(response, 'groups')

    def get_instances(self, api_params: dict):
        if api_params['id'] is not None:
            path = '{0}/{1}'.format(INSTANCES_PATH, api_params['id'])
            try:
                detail = str(api_params['details']).lower()
            except KeyError:
                detail = 'false'
            params = self._url_params({
                'details': detail
            })
            path = self._build_url(path, params)
            response = self.connection.send_request(path=path)
            return self._return_reponse_key(response, 'instance')

        params = mf.dict_keys_to_camel_case(api_params)
        params['max'] = -1
        url_params = self._url_params(params)

        path = self._build_url(INSTANCES_PATH, url_params)

        response = self.connection.send_request(path=path)
        return self._return_reponse_key(response, 'instances')

    def get_instance_snapshots(self, instance_id: int):
        path = '{0}/{1}/snapshots'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path)
        return self._return_reponse_key(response, 'snapshots')

    def get_integrations(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(INTEGRATIONS_PATH, api_params['id'])
            return self._return_reponse_key(response, 'integration')

        # max = -1 doesnt' seem to work on this endpoint
        api_params['max'] = 10000
        response = self._get_object(INTEGRATIONS_PATH, api_params)
        return self._return_reponse_key(response, 'integrations')

    def get_key_pairs(self, api_params: dict):
        params = mf.dict_keys_to_camel_case(api_params)

        if params['id'] is not None:
            path = '{0}/{1}'.format(KEY_PAIR_PATH, params['id'])
            response = self.connection.send_request(path=path)
            return self._return_reponse_key(response, 'keyPair')

        url_params = self._url_params(params)
        path = self._build_url(KEY_PAIR_PATH, url_params)

        response = self.connection.send_request(path=path)
        return self._return_reponse_key(response, 'keyPairs')

    def get_roles(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(ROLES_PATH, api_params['id'])
            return self._return_reponse_key(response, 'role')

        response = self._get_object(ROLES_PATH, api_params, True)
        return self._return_reponse_key(response, 'roles')

    def get_ssl_certificates(self, api_params: dict):
        params = mf.dict_keys_to_camel_case(api_params)

        if params['id'] is not None:
            path = '{0}/{1}'.format(SSL_CERTIFICATES_PATH, params['id'])
            response = self.connection.send_request(path=path)
            return self._return_reponse_key(response, 'certificate')

        url_params = self._url_params(params)
        path = self._build_url(SSL_CERTIFICATES_PATH, url_params)

        response = self.connection.send_request(path=path)
        return self._return_reponse_key(response, 'certificates')

    def get_tenants(self, api_params: dict):
        if api_params['id'] is not None:
            response = self._get_object_by_id(TENANTS_PATH, api_params['id'])
            return self._return_reponse_key(response, 'account')

        response = self._get_object(TENANTS_PATH, api_params, True)
        return self._return_reponse_key(response, 'accounts')

    def get_virtual_images(self, api_params: dict):
        params = mf.dict_keys_to_camel_case(api_params)
        params['max'] = -1

        if params['virtualImageId'] is not None:
            path = '{0}/{1}'.format(VIRTUAL_IMAGES_PATH, params['virtualImageId'])
            response = self.connection.send_request(path=path)
            return self._return_reponse_key(response, 'virtualImage')

        url_params = self._url_params(params)
        path = self._build_url(VIRTUAL_IMAGES_PATH, url_params)

        response = self.connection.send_request(path=path)
        return self._return_reponse_key(response, 'virtualImages')

    def lock_instance(self, instance_id: int):
        path = '{0}/{1}/lock'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, '')

    def refresh_cloud(self, api_params: dict):
        path = '{0}/{1}/refresh'.format(CLOUDS, api_params.pop('id'))
        body = self._payload_from_params(api_params)

        response = self.connection.send_request(
            data=body,
            path=path,
            method='POST'
        )

        return self._return_reponse_key(response, '')

    def restart_instance(self, instance_id: int):
        path = '{0}/{1}/restart'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def set_appliance_maintenance_mode(self, enabled: bool):
        params = self._url_params({'enabled': enabled})
        path = self._build_url(MAINTENANCE_MODE_PATH, params)
        response = self.connection.send_request(path=path, method='POST')
        return self._return_reponse_key(response, '')

    def set_appliance_settings(self, api_params: dict):
        payload = self._payload_from_params(api_params)
        body = {'applianceSettings': payload}

        response = self.connection.send_request(
            data=body,
            path=APPLIANCE_SETTINGS_PATH,
            method='PUT'
        )
        return self._return_reponse_key(response, '')

    def set_cloud_datastore(self, api_params: dict):
        path = '{0}/{1}'.format(CLOUD_DATASTORES.format(api_params.pop('zone_id')), api_params.pop('id'))
        payload = self._payload_from_params(api_params)
        body = {'datastore': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )

        return self._return_reponse_key(response, 'datastore')

    def snapshot_instance(self, api_params: dict):
        path = '{0}/{1}/snapshot'.format(INSTANCES_PATH, api_params.pop('id'))
        payload = self._payload_from_params(api_params)
        body = {'snapshot': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )

        return self._return_reponse_key(response, '')

    def snapshot_revert(self, instance_id: int, snapshot_id: int):
        path = '{0}/{1}/revert-snapshot/{2}'.format(INSTANCES_PATH, instance_id, snapshot_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, '')

    def start_instance(self, instance_id: int):
        path = '{0}/{1}/start'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def stop_instance(self, instance_id: int):
        path = '{0}/{1}/stop'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def suspend_instance(self, instance_id: int):
        path = '{0}/{1}/suspend'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, 'results')

    def update_cloud(self, api_params: dict):
        path = '{0}/{1}'.format(CLOUDS, api_params.pop('id'))

        payload = self._payload_from_params(api_params)
        body = {'zone': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )
        return self._return_reponse_key(response, 'zone')

    def update_cloud_logo(self, api_params: dict):
        path = '{0}/{1}/update-logo'.format(CLOUDS, api_params['id'])

        file_data = []

        if api_params['logo'] is not None:
            file_data.append(
                {
                    'name': 'logo',
                    'file_path': api_params['logo']
                }
            )

        if api_params['dark_logo'] is not None:
            file_data.append(
                {
                    'name': 'darkLogo',
                    'file_path': api_params['dark_logo']
                }
            )

        response = self.connection.multipart_upload(
            uri_path=path,
            file_data=file_data
        )

        return self._return_reponse_key(response, '')

    def update_group(self, api_params: dict):
        path = '{0}/{1}'.format(GROUPS_PATH, api_params.pop('id'))

        payload = self._payload_from_params(api_params)
        body = {'group': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )
        return self._return_reponse_key(response, 'group')

    def update_group_zones(self, api_params: dict):
        path = '{0}/{1}/update-zones'.format(GROUPS_PATH, api_params.pop('id'))

        payload = self._payload_from_params(api_params)
        body = {'group': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )
        return self._return_reponse_key(response, '')

    def update_ssl_certificate(self, api_params: dict):
        path = '{0}/{1}'.format(SSL_CERTIFICATES_PATH, api_params.pop('id'))

        payload = self._payload_from_params(api_params)
        body = {'certificate': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )
        return self._return_reponse_key(response, 'certificate')

    def update_virtual_image(self, api_params: dict):
        path = '{0}/{1}'.format(VIRTUAL_IMAGES_PATH, api_params.pop('virtual_image_id'))

        payload = self._payload_from_params(api_params)
        body = {'virtualImage': payload}

        response = self.connection.send_request(
            data=body,
            path=path,
            method='PUT'
        )
        return self._return_reponse_key(response, 'virtualImage')

    def upload_virtual_image_file(self, api_params: dict):
        path = '{0}/{1}/upload'.format(VIRTUAL_IMAGES_PATH, api_params.pop('virtual_image_id'))

        payload = mf.dict_keys_to_camel_case(
            api_params
        )

        response = {}

        if payload['url'] is not None:
            url_params = self._url_params(api_params)
            path = self._build_url(path, url_params)
            response = self.connection.send_request(
                path=path,
                method='POST'
            )

        return self._return_reponse_key(response, '')

    def unlock_instance(self, instance_id: int):
        path = '{0}/{1}/unlock'.format(INSTANCES_PATH, instance_id)
        response = self.connection.send_request(path=path, method='PUT')
        return self._return_reponse_key(response, '')
