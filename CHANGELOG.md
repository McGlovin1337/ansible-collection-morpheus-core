# Changelog

## v0.x.x
- Added `virtual_image_info` module

## v0.5.0
- Added `instance` module
- Added `instance_snapshot_info` module
- Added `instance_snapshot` module

## v0.4.0
- Added `appliance_settings` module
- Added `appliance_maintenance_mode` module
- Added `instance_info` module

## v0.3.0
- Added httpapi connection plugin
- Added `appliance_facts` module

## v0.2.5
- Added AWS assume role support to cloud role

## v0.2.4
- Added `baseRoleId` to `userroles` role

## v0.2.3
- Verbose messages caused a problem with the app search type: [#26](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/26)

## v0.2.2

- In 5.4.3, Morpheus is requiring authentication for version information from `/api/ping`: [#7](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/7)
- OS Type is now able to be set via name in `roles/virtualimages`: [#6](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/6)
- Ansible requires that the FQCN be in the documentation part of the inventory plugin: [#3](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/3)
- `roles/settings` had the wrong source var: [#2](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/2)
- Version comparison was using distutils, which has been deprecated.  Switched to packaging. [#10](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/10)
- Troubleshooting info and verbose messaging added to plugin with `-vv` or higher. [#15](https://github.com/gomorpheus/ansible-collection-morpheus-core/issues/15)
