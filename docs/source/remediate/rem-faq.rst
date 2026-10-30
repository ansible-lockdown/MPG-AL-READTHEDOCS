Remediate - FAQ
===============

.. contents::
   :local:
   :backlinks: none

Connection and Authentication Issues
------------------------------------

Missing Sudo Password (Linux OS Based)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many of the CIS Linux OS based roles remove the ability for sudoers to use the NOPASSWD option to enable elevated privileges.

The user (unless root) that is running the playbook on the target should have a password set and the playbook run accordingly to pass the become_password.

.. code-block:: console

   ansible-playbook -i inventory site.yml --ask-become-pass

All repositories should now run a pre-req check to ensure that the user does have a password set and will fail if this is not setup.

SSH Connection Timeout
^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [host]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh"}

**Common Causes:**

- SSH service not running on target
- Firewall blocking SSH port
- Incorrect SSH key or credentials
- Host key verification failure

**Solutions:**

.. code-block:: console

   # Test SSH connectivity directly
   ssh -v user@target_host

   # Skip host key checking (use with caution)
   ansible-playbook -i inventory site.yml -e 'ansible_ssh_common_args="-o StrictHostKeyChecking=no"'

   # Increase connection timeout
   ansible-playbook -i inventory site.yml -e 'ansible_timeout=60'

WinRM Connection Failed (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [windows_host]: UNREACHABLE! => {"changed": false, "msg": "winrm connection error"}

**Solutions:**

1. Verify WinRM is configured on the target:

.. code-block:: powershell

   # On Windows target
   winrm quickconfig

Use HTTPS (port 5986) or NTLM/Kerberos with message encryption. Do not rely on Basic
authentication or unencrypted WinRM traffic: the Windows CIS and STIG roles disable both
(for example Windows-2022-CIS 18.10.89.2.1 and 18.10.89.2.3, Windows-2022-STIG
WN22-CC-000500 and WN22-CC-000510), so a connection that depends on them breaks during the run.

2. Check your inventory variables (INI inventory):

.. code-block:: ini

   [windows:vars]
   ansible_connection=winrm
   ansible_port=5986
   ansible_winrm_transport=ntlm
   ansible_winrm_server_cert_validation=ignore

Windows-2022-CIS also lists ``pypsrp`` on the controller as an alternative to ``pywinrm`` (``ansible_connection=psrp``).

Python Interpreter Not Found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [host]: FAILED! => {"msg": "Ansible requires Python 3.9 or newer on the target. Current version: ..."}

The minimum Python version depends on the ansible-core version in use.

**Solution:**

Specify a supported Python interpreter explicitly:

.. code-block:: yaml

   # In host_vars or group_vars
   ansible_python_interpreter: /usr/bin/python3

Or use interpreter discovery:

.. code-block:: yaml

   ansible_python_interpreter: auto_silent

Module Not Found Errors
^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: text

   [ERROR]: couldn't resolve module/action 'community.general.xxx'. This often indicates a misspelling, missing collection, or incorrect module path.

**Solution:**

Install the collections listed in the role's ``collections/requirements.yml`` (run from the role directory):

.. code-block:: console

   ansible-galaxy collection install -r collections/requirements.yml

Playbook Execution Issues
-------------------------

Task Fails with "Permission Denied"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [host]: FAILED! => {"msg": "Permission denied"}

**Solutions:**

1. Ensure become is enabled:

.. code-block:: yaml

   - hosts: all
     become: true
     roles:
       - RHEL10-CIS

2. Verify sudo configuration on target:

.. code-block:: console

   # On target host
   sudo -l

3. Check SELinux/AppArmor isn't blocking:

.. code-block:: console

   # Check SELinux denials
   ausearch -m avc -ts recent

Idempotency Warnings
^^^^^^^^^^^^^^^^^^^^

**Symptom:** Tasks report "changed" on every run when they shouldn't.

**Common Causes:**

- File permissions or ownership drift
- Services being restarted unnecessarily
- Configuration files being regenerated

**Solution:**

This is usually expected behavior for certain controls. To verify idempotency:

.. code-block:: console

   # Run playbook twice
   ansible-playbook site.yml
   ansible-playbook site.yml

   # Second run should show minimal changes

Configuration and Variable Issues
---------------------------------

How Do I Skip Specific Controls?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the control variable to ``false`` in your playbook or extra vars:

**CIS Example (RHEL10-CIS):**

.. code-block:: yaml

   # Skip specific CIS controls
   rhel10cis_rule_1_1_1_1: false
   rhel10cis_rule_5_2_4: false

**STIG Example (RHEL10-STIG):**

.. code-block:: yaml

   # Skip specific STIG controls
   rhel10stig_000530: false
   rhel10stig_001020: false

Toggle names differ between roles (for example ``rhel_09_171011`` in RHEL9-STIG and
``rhel8stig_010382`` in RHEL8-STIG). Use the names in the role's ``defaults/main/main.yml``.

**Skip entire categories:**

.. code-block:: yaml

   # STIG - Skip CAT III controls (RHEL10-STIG)
   rhel10stig_cat3: false

To skip CIS Level 2 controls, use tags:

.. code-block:: console

   ansible-playbook site.yml --skip-tags level2-server,level2-workstation

How Do I Change Default Values?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Override variables in your playbook or create a vars file:

.. code-block:: yaml

   # playbook.yml
   - hosts: all
     become: true
     vars:
       rhel10cis_start_chronyd: true
       rhel10cis_sshd_clientaliveinterval: 300
       rhel10cis_passwd_minlen_value: 14
     roles:
       - RHEL10-CIS

Or use extra vars:

.. code-block:: console

   ansible-playbook site.yml -e '{"rhel10cis_sshd_clientaliveinterval":300}'

Variable Precedence Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** Your variable overrides aren't being applied.

**Solution:**

Ansible has a specific variable precedence order. From lowest to highest:

1. Role defaults (``defaults/main.yml``)
2. Inventory vars
3. Playbook vars
4. Extra vars (``-e``) - **highest precedence**

Use extra vars to guarantee override. Pass booleans in JSON form; ``key=value`` passes the
string ``"false"``, which fails as a conditional:

.. code-block:: console

   ansible-playbook site.yml -e '{"rhel10cis_rule_1_1_1_1": false}'

Service and System Issues
-------------------------

Users Locked Out After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

- PAM configuration changes (password complexity, lockout)
- SSH configuration changes (allowed users/groups)
- sudo configuration changes

**Solutions:**

1. Verify SSH allows your user:

.. code-block:: console

   sudo sshd -T | grep -iE "allowusers|allowgroups|denyusers|denygroups"

2. Check PAM lockout status:

.. code-block:: console

   faillock --user <username>
   faillock --user <username> --reset

3. Review sudo configuration:

.. code-block:: console

   visudo -c
   cat /etc/sudoers.d/*

Where Can I Get More Help?
--------------------------

- `Discord Community <https://www.lockdownenterprise.com/discord>`_ - Community support
- `GitHub Issues <https://github.com/ansible-lockdown>`_ - Report bugs or request features
- `Lockdown Enterprise <https://www.lockdownenterprise.com>`_ - Commercial support options
