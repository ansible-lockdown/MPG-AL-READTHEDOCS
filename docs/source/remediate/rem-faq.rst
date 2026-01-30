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
   winrm set winrm/config/service '@{AllowUnencrypted="true"}'
   winrm set winrm/config/service/auth '@{Basic="true"}'

2. Check your inventory variables:

.. code-block:: yaml

   [windows:vars]
   ansible_connection=winrm
   ansible_winrm_server_cert_validation=ignore
   ansible_winrm_transport=ntlm

Python and Dependency Issues
----------------------------

Missing "jmespath" Fatal Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   fatal: [ansible]: FAILED! => {"msg": "You need to install \"jmespath\" prior to running json_query filter"}

This can occur during a playbook run on certain operating systems when patching takes place as part of the playbook due to the way python is implemented.

* `You Need to install jmespath <https://serverfault.com/questions/1114638/ansible-you-need-to-install-jmespath-prior-to-running-json-query-filter-bu>`_ : A great article and explanation written by Discord community member baassssiiee

.. note::

   This should no longer be an issue with new releases as the dependency has been removed.

Python Interpreter Not Found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [host]: FAILED! => {"msg": "ansible-core requires a minimum of Python version 3.10"}

**Solution:**

Specify the Python interpreter explicitly:

.. code-block:: yaml

   # In inventory or host_vars
   ansible_python_interpreter=/usr/bin/python3

Or use interpreter discovery:

.. code-block:: yaml

   ansible_python_interpreter=auto_silent

Module Not Found Errors
^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   ERROR! couldn't resolve module/action 'community.general.xxx'

**Solution:**

Install required collections:

.. code-block:: console

   ansible-galaxy collection install community.general
   ansible-galaxy collection install ansible.posix

Playbook Execution Issues
-------------------------

Playbook Hangs or Runs Forever
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

- Control waiting for user input (interactive prompts)
- Package manager waiting for confirmation
- Service restart hanging

**Solutions:**

1. Use non-interactive package installations:

.. code-block:: yaml

   # Already handled in roles, but verify environment
   DEBIAN_FRONTEND: noninteractive

2. Add timeouts to long-running tasks:

.. code-block:: console

   ansible-playbook site.yml -e 'ansible_timeout=300'

3. Run with verbose output to identify stuck task:

.. code-block:: console

   ansible-playbook site.yml -vvv

Task Fails with "Permission Denied"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   fatal: [host]: FAILED! => {"msg": "Permission denied"}

**Solutions:**

1. Ensure become is enabled:

.. code-block:: yaml

   - hosts: all
     become: yes
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

**CIS Example:**

.. code-block:: yaml

   # Skip specific CIS controls
   rhel10cis_rule_1_1_1_1: false
   rhel10cis_rule_5_2_4: false

**STIG Example:**

.. code-block:: yaml

   # Skip specific STIG controls
   rhel_10_010010: false
   rhel_10_020000: false

**Skip entire categories:**

.. code-block:: yaml

   # CIS - Skip all Level 2 controls
   rhel10cis_level_2: false

   # STIG - Skip CAT III controls
   rhel10stig_cat3_patch: false

How Do I Change Default Values?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Override variables in your playbook or create a vars file:

.. code-block:: yaml

   # playbook.yml
   - hosts: all
     become: yes
     vars:
       rhel10cis_time_sync_tool: chrony
       rhel10cis_sshd_client_alive_interval: 300
       rhel10cis_password_min_length: 14
     roles:
       - RHEL10-CIS

Or use extra vars:

.. code-block:: console

   ansible-playbook site.yml -e '{"rhel10cis_time_sync_tool":"chrony"}'

Variable Precedence Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** Your variable overrides aren't being applied.

**Solution:**

Ansible has a specific variable precedence order. From lowest to highest:

1. Role defaults (``defaults/main.yml``)
2. Inventory vars
3. Playbook vars
4. Extra vars (``-e``) - **highest precedence**

Use extra vars to guarantee override:

.. code-block:: console

   ansible-playbook site.yml -e 'rhel10cis_rule_1_1_1_1=false'

Service and System Issues
-------------------------

Services Fail to Start After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** Application services won't start after running hardening playbook.

**Common Causes:**

- SELinux policy changes
- Firewall rules blocking ports
- File permission changes
- PAM configuration changes

**Troubleshooting Steps:**

1. Check service status and logs:

.. code-block:: console

   systemctl status <service_name>
   journalctl -xeu <service_name>

2. Check SELinux denials:

.. code-block:: console

   ausearch -m avc -ts recent
   sealert -a /var/log/audit/audit.log

3. Verify firewall rules:

.. code-block:: console

   firewall-cmd --list-all

4. Review the specific control that may have affected your service and disable if needed.

System Won't Boot After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Prevention:**

.. warning::

   Always test hardening in non-production environments first!

**Common Causes:**

- GRUB password configured but not documented
- Filesystem mount options preventing boot
- Kernel parameter changes

**Recovery Steps:**

1. Boot into rescue mode
2. Review ``/etc/default/grub`` for kernel parameters
3. Check ``/etc/fstab`` for mount option issues
4. Review ``/etc/security/limits.conf`` for restrictive limits

Users Locked Out After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

- PAM configuration changes (password complexity, lockout)
- SSH configuration changes (allowed users/groups)
- sudo configuration changes

**Solutions:**

1. Verify SSH allows your user:

.. code-block:: console

   grep -E "AllowUsers|AllowGroups|DenyUsers|DenyGroups" /etc/ssh/sshd_config

2. Check PAM lockout status:

.. code-block:: console

   faillock --user <username>
   faillock --user <username> --reset

3. Review sudo configuration:

.. code-block:: console

   visudo -c
   cat /etc/sudoers.d/*

Performance Issues
------------------

Playbook Takes Too Long
^^^^^^^^^^^^^^^^^^^^^^^

**Solutions:**

1. Use strategy plugins for parallelism:

.. code-block:: yaml

   # ansible.cfg
   [defaults]
   strategy = free
   forks = 20

2. Limit to specific tags:

.. code-block:: console

   # Run only SSH-related controls
   ansible-playbook site.yml --tags ssh

3. Skip fact gathering if not needed:

.. code-block:: yaml

   - hosts: all
     gather_facts: no

High CPU/Memory During Execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The hardening playbooks can be resource-intensive. Solutions:

1. Limit parallel execution:

.. code-block:: console

   ansible-playbook site.yml --forks 5

2. Run during maintenance windows

3. Consider running in batches using ``serial``:

.. code-block:: yaml

   - hosts: all
     serial: 10

Rollback and Recovery
---------------------

How Do I Undo Hardening Changes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The roles do not include automatic rollback functionality. Options:

1. **Restore from backup/snapshot** (recommended)
   - Take VM snapshots before hardening
   - Use configuration management baseline

2. **Selectively reverse changes**
   - Identify specific controls causing issues
   - Manually reverse those configurations

3. **Re-image the system**
   - For immutable infrastructure, redeploy from base image

.. tip::

   Always maintain system backups or snapshots before applying hardening roles.

Where Can I Get More Help?
--------------------------

- `Discord Community <https://www.lockdownenterprise.com/discord>`_ - Community support
- `GitHub Issues <https://github.com/ansible-lockdown>`_ - Report bugs or request features
- `Lockdown Enterprise <https://lockdownenterprise.com>`_ - Commercial support options
