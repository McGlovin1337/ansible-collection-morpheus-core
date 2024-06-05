
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.9.0

.. Anchors

.. _ansible_collections.morpheus.core.search_lookup:

.. Anchors: short name for ansible.builtin

.. Title

morpheus.core.search lookup -- Lookup various Morpheus items
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `morpheus.core collection <https://galaxy.ansible.com/ui/repo/published/morpheus/core/>`_ (version 0.7.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install morpheus.core`.

    To use it in a playbook, specify: :code:`morpheus.core.search`.

.. version_added

.. rst-class:: ansible-version-added

New in morpheus.core 0.x.x

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Search for various Morpheus items.


.. Aliases


.. Requirements




.. Terms

Terms
-----

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-_terms"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-_terms:

      .. rst-class:: ansible-option-title

      **Terms**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The search terms to lookup.


      .. raw:: html

        </div>





.. Options

Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('morpheus.core.search', key1=value1, key2=value2, ...)`` and ``query('morpheus.core.search', key1=value1, key2=value2, ...)``

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-morpheus_host"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-morpheus_host:

      .. rst-class:: ansible-option-title

      **morpheus_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-morpheus_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Morpheus Hostname or IP Address to query.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`ANSIBLE\_MORPHEUS\_HOST`

      - Variable: ansible\_morpheus\_host


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-morpheus_password"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-morpheus_password:

      .. rst-class:: ansible-option-title

      **morpheus_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-morpheus_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Password for the \ :ansopt:`morpheus.core.search#lookup:morpheus\_user`\  to connect to the Morpheus Appliance.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`ANSIBLE\_MORPHEUS\_PASSWORD`

      - Variable: ansible\_morpheus\_password


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-morpheus_token"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-morpheus_token:

      .. rst-class:: ansible-option-title

      **morpheus_token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-morpheus_token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specify an API Token instead of \ :ansopt:`morpheus.core.search#lookup:morpheus\_user`\  or \ :ansopt:`morpheus.core.search#lookup:morpheus\_password`\  parameters.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`ANSIBLE\_MORPHEUS\_TOKEN`

      - Variable: ansible\_morpheus\_token


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-morpheus_user"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-morpheus_user:

      .. rst-class:: ansible-option-title

      **morpheus_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-morpheus_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Username to connect to the Morpheus Appliance.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`ANSIBLE\_MORPHEUS\_USER`

      - Variable: ansible\_morpheus\_user


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_item"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-search_item:

      .. rst-class:: ansible-option-title

      **search_item**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_item" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The item type to search/lookup.

      By default this is a general global search of the Morpheus Appliance.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"app"`
      - :ansible-option-choices-entry:`"blueprint"`
      - :ansible-option-choices-entry:`"cloud"`
      - :ansible-option-choices-entry:`"cloud\_type"`
      - :ansible-option-choices-entry:`"environment"`
      - :ansible-option-choices-entry-default:`"global"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"group"`
      - :ansible-option-choices-entry:`"host"`
      - :ansible-option-choices-entry:`"instance"`
      - :ansible-option-choices-entry:`"instance\_type"`
      - :ansible-option-choices-entry:`"integration"`
      - :ansible-option-choices-entry:`"layout"`
      - :ansible-option-choices-entry:`"network"`
      - :ansible-option-choices-entry:`"network\_group"`
      - :ansible-option-choices-entry:`"node\_type"`
      - :ansible-option-choices-entry:`"plugin"`
      - :ansible-option-choices-entry:`"policy"`
      - :ansible-option-choices-entry:`"role"`
      - :ansible-option-choices-entry:`"task"`
      - :ansible-option-choices-entry:`"tenant"`
      - :ansible-option-choices-entry:`"virtual\_image"`
      - :ansible-option-choices-entry:`"workflow"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-use_ssl"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-use_ssl:

      .. rst-class:: ansible-option-title

      **use_ssl**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-use_ssl" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Connect to Morpheus Appliance using an HTTPS/SSL Connection.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.morpheus.core.search_lookup__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Control whether to validate Morpheus Appliance SSL Certificates.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters:
     ``lookup('morpheus.core.search', term1, term2, key1=value1, key2=value2)`` and ``query('morpheus.core.search', term1, term2, key1=value1, key2=value2)``
   - When used with the 'morpheus.core.morpheus' httpapi plugin the \ :ansopt:`morpheus.core.search#lookup:morpheus\_user`\ , \ :ansopt:`morpheus.core.search#lookup:morpheus\_password`\ , and \ :ansopt:`morpheus.core.search#lookup:morpheus\_token`\  parameters can be omitted with the value of \ :ansopt:`morpheus.core.search#lookup:morpheus\_host`\  set to \ :ansval:`inventory\_hostname`\ .

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Find items with the term "instance"
      ansible.builtin.debug:
        msg: "{{ q('morpheus.core.search', 'instance', morpheus_token='abcd...', morpheus_instance='cmp.domain.tld') }}"

    - name: Search current Morpheus Appliance when used with httpapi plugin
      ansible.builtin.debug:
        msg: "{{ q('morpheus.core.search', 'instance', morpheus_instance=inventory_hostname) }}"

    - name: Search for Instances with "Apache" in their name
      ansible.builtin.debug:
        msg: "{{ q('morpheus.core.search', 'Apache', search_type='instance', morpheus_instance=inventory_hostname) }}"




.. Facts


.. Return values

Return Value
------------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-_list"></div>

      .. _ansible_collections.morpheus.core.search_lookup__return-_list:

      .. rst-class:: ansible-option-title

      **Return value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_list" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of matching items.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- James Riach (@McGlovin1337)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Repository (Sources)"
    url: "https://www.github.com/gomorpheus/ansible-collection-morpheus-core"
    external: true


.. Parsing errors

