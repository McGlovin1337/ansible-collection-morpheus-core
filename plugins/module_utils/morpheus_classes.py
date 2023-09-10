from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
name: morph_api_classes
short_description: Shared Morpheus API Classes
description:
    - Shared Classes for Morpheus API Modules
version_added: 0.x.x
author: James Riach
'''

from datetime import datetime
try:
    from morpheusapi import dict_keys_to_snake_case
except ModuleNotFoundError:
    from ansible_collections.morpheus.core.plugins.module_utils.morpheusapi import dict_keys_to_snake_case


class InstanceSnapshots():
    def __init__(self, instance_name: str, instance_id: int, snapshots: list[dict]) -> None:
        self.instance_name = instance_name
        self.instance_id = instance_id
        self.snapshot_count = len(snapshots)
        self.snapshots = [dict_keys_to_snake_case(snapshot) for snapshot in snapshots]

    def sort(self, reverse: bool = False) -> None:
        """Sorts the list of snapshots by datetime

        Args:
            reverse (bool, optional): Reverses the sort order, i.e. most recent datetime first. Defaults to False.
        """
        date_format = '%Y-%m-%dT%H:%M:%SZ'

        self.snapshots.sort(
            key=lambda dt: datetime.strptime(dt['date_created'], date_format),
            reverse=reverse
        )


class SnapshotAction():
    """
    A Class for managing Instance Snapshots and performing various actions against them.
    """
    def __init__(self, morpheus_api: MorpheusApi, action: str,
                 instance_id: int = None, instance_name: str = None,
                 snapshot_id: int = None, snapshot_name: str = None,
                 snapshot_date: str = None, snapshot_description: str = None) -> None:
        self._morpheus_api = morpheus_api
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.snapshot_id = snapshot_id
        self.snapshot_name = snapshot_name
        self.snapshot_date = snapshot_date
        self.snapshot_description = snapshot_description
        self.action = action
        self.msg = ''
        self.success = False

    def _create(self):
        response = self._morpheus_api.snapshot_instance({
            'id': self.instance_id,
            'name': self.snapshot_name,
            'description': self.snapshot_description
        })
        self.success, self.msg = success_response(response)

    def _remove(self):
        response = self._morpheus_api.delete_snapshot(self.snapshot_id)
        self.success, self.msg = success_response(response)

    def _remove_all(self):
        response = self._morpheus_api.delete_all_instance_snapshots(self.instance_id)
        self.success, self.msg = success_response(response)

    def _revert(self):
        response = self._morpheus_api.snapshot_revert(
            self.instance_id,
            self.snapshot_id
        )
        self.success, self.msg = success_response(response)

    def execute(self) -> dict:
        """Perform the required action against the Snapshot

        Returns:
            dict: A Dictionary based on the Class Attributes
        """
        action = {
            'create': self._create,
            'remove': self._remove,
            'remove_all': self._remove_all,
            'revert': self._revert
        }.get(self.action)

        action()

        results = vars(self)
        del results['_morpheus_api']
        del results['snapshot_description']
        return results
    