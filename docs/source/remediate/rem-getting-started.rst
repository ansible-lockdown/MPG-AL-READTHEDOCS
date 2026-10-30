Remediate
=========

This role is part of the `Ansible Lockdown`_ project and can be used as a
standalone role or it can be used along with other Ansible roles, playbooks, or collections.

.. _Ansible Lockdown: https://github.com/ansible-lockdown

.. contents::
   :local:
   :backlinks: none

.. warning::

    It is strongly recommended to run the role in a test environment first. There are controls that could introduce
    breaking changes. Check mode might not always catch these changes. The best way to confirm how the role will change
    your system is to fully test.

Requirements
------------

This documentation assumes that the reader has completed the steps within the

* `Ansible installation guide <https://docs.ansible.com/ansible/latest/installation_guide/index.html>`_.

and has a good understanding of using ansible

* `Getting started with Ansible <https://docs.ansible.com/projects/ansible/latest/getting_started/index.html>`_.

.. note::

    The role requires elevated privileges and must be run as a user with ``sudo``
    access. The playbook examples below set ``become: true``, which causes Ansible to use
    sudo before running tasks.

The roles require ansible-core 2.16.1 or newer (``min_ansible_version`` in each role's
``meta/main.yml``). Install the collections a role needs from its own requirements file:

.. code-block:: console

   ansible-galaxy collection install -r collections/requirements.yml

Installation
------------

The recommended installation methods for this role are
``ansible-galaxy`` (recommended) or ``git``.

Using ``ansible-galaxy``
~~~~~~~~~~~~~~~~~~~~~~~~

The easiest installation method is to use the ``ansible-galaxy`` command that
is provided with your Ansible installation:

The general format is ansible-galaxy install git+|url to repo|, below is an example with
RHEL10-CIS

.. code-block:: console

   ansible-galaxy install git+https://github.com/ansible-lockdown/RHEL10-CIS.git

The ``ansible-galaxy`` command installs the role into the first writable
directory in ``roles_path``, by default ``~/.ansible/roles``, which makes it
easy to use with Ansible playbooks.

Using ``git``
~~~~~~~~~~~~~

Start by cloning the role into a directory of your choice. This example uses ``~/CIS_Roles``,
which can be changed to any folder.

To clone and create a folder with the same name as the repo:

.. code-block:: console

   mkdir -p ~/CIS_Roles
   cd ~/CIS_Roles
   git clone https://github.com/ansible-lockdown/RHEL10-CIS.git

To clone into a folder with a different name (the folder must be empty or not exist yet):

.. code-block:: console

   git clone https://github.com/ansible-lockdown/RHEL10-CIS.git ~/CIS_Roles/my-rhel10-cis

Ansible looks for roles in ``~/.ansible/roles`` by default.

If the role is cloned into a different directory, that directory must be
provided with the ``roles_path`` option in ``ansible.cfg``. The following is
an example of a ``ansible.cfg`` file that uses a custom path for roles:

.. code-block:: ini

   [defaults]
   roles_path = /etc/ansible/roles:/home/myuser/custom/roles

With this configuration, Ansible looks for roles in ``/etc/ansible/roles`` and
``/home/myuser/custom/roles``.

How to Use
----------

On Its Own
~~~~~~~~~~

This role can be used on its own as a role. The file ``site.yml`` is the included file to point to. This role does not include an inventory file for hosts
since that is too site specific, that will need to be managed locally. Below are examples of how to run in various scenarios

CLI - Notice the reference to site.yml

.. code-block:: console

  cd roles
  ansible-playbook -i hosts -e '{ "rhel10cis_section1":false,"rhel10cis_section2":false }' ./RHEL10-CIS/site.yml

With Existing Playbooks
~~~~~~~~~~~~~~~~~~~~~~~

This role works well with existing playbooks. The following is an
example of a basic playbook that uses this role:

.. code-block:: yaml

    ---

    - hosts: servers
      become: true
      roles:
        - role: RHEL10-CIS
          when:
            - ansible_facts['os_family'] == 'RedHat'
            - ansible_facts['distribution_major_version'] is version('10', '==')

Variables and the Role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The role is fully customizable by setting the variables provided in the ``defaults/main.yml`` file. These variables range in usage from toggling entire sections (CIS), categories (STIG), general groups (GUI related), individual controls, localized settings, etc.
There are comments around these variables that have a description of what the variable does, what the value options are, and what controls are associated with the variable.
Variables are also listed in order of appearance in the execution of the role, variables used early in the role are listed earlier in the file. Variables in this location are also very low in precedence,
`here is the official list of variable precedence. <https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence>`_
This means they are overwritten very easily via extra vars.

This role has been written with ease of use in mind, which means it's written in a way that requires as little user interaction as possible. No need to modify any tasks at all!


Using and Modifying Variables Directly (``defaults/main.yml``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the most basic way to make the change. The file has all of the available variables along with comments on what task the variable is for, a description on what the variable is, and
the formatting for the value in the variable. Just update the values as needed

Modifying Variables with Extra-Vars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is where the power of using variables via ``defaults/main.yml`` come into play. Anywhere you can use or set an extra var is place you can set these variables.

CLI In-Line setting (Set to only run STIG CAT1, RHEL10-STIG)

.. code-block:: console

  ansible-playbook -i host_file -e '{ "rhel10stig_cat2":false,"rhel10stig_cat3":false }' ./RHEL10-STIG/site.yml

Using Tags
~~~~~~~~~~
Each  control is tagged with various pieces of information about the control to allow for more refined use with skipping or running controls.
For STIG this includes all of the IDs, CIS has the level2 data, and both have info related to what the control relates to. For example all controls related to SSH will have the ``ssh`` tag.

STIG Example (RHEL10-STIG, RHEL-10-000530):

.. code-block:: yaml

    tags:
      - RHEL-10-000530
      - CAT2
      - CCI-002385
      - SRG-OS-000420-GPOS-00186
      - SV-280937r1184727_rule
      - V-280937
      - NIST800-53R4_SC-5

CIS Example (RHEL10-CIS, 2.1.4):

.. code-block:: yaml

  tags:
      - level1-server
      - level1-workstation
      - automated
      - patch
      - dhcp
      - NIST800-53R5_CM-7
      - rule_2.1.4
