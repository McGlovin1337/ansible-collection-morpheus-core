from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    id:
        description:
            - Return specific object by id.
        type: int
    name:
        description:
            - Filter by name.
        type: string
    regex_name:
        description:
            - Treat the name parameter as a regular expression.
        default: false
        type: bool
'''
