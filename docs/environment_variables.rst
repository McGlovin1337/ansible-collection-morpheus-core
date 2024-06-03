
:orphan:

.. meta::
  :antsibull-docs: 2.9.0

.. _list_of_collection_env_vars:

Index of all Collection Environment Variables
=============================================

The following index documents all environment variables declared by plugins in collections.
Environment variables used by the ansible-core configuration are documented in :ref:`ansible_configuration_settings`.

.. envvar:: ANSIBLE_MORPHEUS_HOST

    The Morpheus Hostname or IP Address to query.

    *Used by:*
    :ansplugin:`morpheus.core.search lookup plugin <morpheus.core.search#lookup>`
.. envvar:: ANSIBLE_MORPHEUS_PASSWORD

    The Password for the \ :ansopt:`morpheus\_user`\  to connect to the Morpheus Appliance.

    *Used by:*
    :ansplugin:`morpheus.core.search lookup plugin <morpheus.core.search#lookup>`
.. envvar:: ANSIBLE_MORPHEUS_TOKEN

    See the documentations for the options where this environment variable is used.

    *Used by:*
    :ansplugin:`morpheus.core.morpheus httpapi plugin <morpheus.core.morpheus#httpapi>`,
    :ansplugin:`morpheus.core.search lookup plugin <morpheus.core.search#lookup>`
.. envvar:: ANSIBLE_MORPHEUS_USER

    The Username to connect to the Morpheus Appliance.

    *Used by:*
    :ansplugin:`morpheus.core.search lookup plugin <morpheus.core.search#lookup>`
