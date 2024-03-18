from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    state:
        description:
            - Create, Update or Remove a Cloud.
        choices:
            - present
            - absent
            - refresh
        default: present
    id:
        description:
            - Specify an existing Cloud to Update or Remove.
        type: int
        aliases:
            - cloud_id
            - zone_id
    name:
        description:
            - Set the name of the Cloud.
        type: string
    description:
        description:
            - Set the description of the Cloud.
        type: string
    code:
        description:
            - The code to reference the Cloud for use in polcies etc.
        type: string
    location:
        description:
            - Add location information for the Cloud.
        type: string
    visibility:
        description:
            - Toggle tenant visibility between Private or Public.
        choices:
            - private
            - public
        type: string
    group_id:
        description:
            - Set the Cloud Group this Cloud is a member of.
        type: int
    account_id:
        description:
            - Set the tenant for which Cloud is assigned to.
        type: int
        aliases:
            - tenant_id
    enabled:
        description:
            - Enable O(enabled=true) or Disable O(enabled=false) the Cloud.
        type: bool
    agent_mode:
        description:
            - Agent Install Mode.
            - V(cloudinit) and V(unattend) are the same.
            - V(guestexec), V(ssh) and V(winrm) are the same.
        choices:
            - cloudinit
            - guestexec
            - ssh
            - winrm
            - unattend
        type: string
    appliance_url:
        description:
            - URL of the Morpheus Appliance.
        type: string
    auto_recover_power_state:
        description:
            - Automatically Power-on Virtual Machines.
        type: bool
    costing_mode:
        description:
            - Enable costing on the Cloud.
        choices:
            - off
            - costing
        type: string
        aliases:
            - costing
    datacenter_name:
        description:
            - Custom Datacenter Identifier.
        type: string
    guidence_mode:
        description:
            - Enable/Disable Cloud Guidance
        choices:
            - off
            - manual
        type: string
        aliases:
            - guidance
    scale_priority:
        description:
            - Set Scale Priority.
        type: int
    security_mode:
        description:
            - Host firewall.
        choices:
            - off
            - internal
        type: string
    timezone:
        description:
            - The Time Zone of the Cloud.
        type: string
    logo:
        description:
            - Path to an image file to use as the Cloud logo.
        type: string
    dark_logo:
        description:
            - Path to an image file to use as the Cloud logo when in dark mode.
        type: string
    remove_resources:
        description:
            - Relevant when O(state=absent), remove associated resources when removing the cloud.
            - Includes removal of Virtual Machines and other forms of Compute.
        type: bool
        default: false
    force_remove:
        description:
            - Force removal if Cloud is still in a group.
        type: bool
        default: false
    refresh_mode:
        description:
            - The type of refresh to perform.
            - V(costing) Pull costing data.
            - V(costing_rebuild) Purge existing costing data and rebuild by calling the Cloud API.
            - V(daily) Perform a daily Cloud Sync.
            - V(hourly) Perform hourly Cloud Sync.
        type: string
        choices:
            - costing
            - costing_rebuild
            - daily
            - hourly
        default: hourly
    refresh_period:
        description:
            - The invoice billing period to refresh.
            - The value should be in the format of YYYYMM.
        type: int
'''
