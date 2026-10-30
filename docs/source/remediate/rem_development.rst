How to Contribute to Remediate Development
------------------------------------------

Remediate Code Summary
~~~~~~~~~~~~~~~~~~~~~~

We strive to maintain a set of standards and consistency for all code that is written. Please review the formatting of previously written controls
and follow the formatting currently in place. We do have a style guide on writing controls that document standard linting, parameter use/order, tagging, etc.

Remediate Code Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Keep it as simple as possible**

  - This is to aid investigation and debugging. Overly complicated tasks/controls are harder to troubleshoot when things go wrong.

- **Readability is key**

  - This means the most clever way to write something might lead to the task being complicated and hard to read.
  - For example if you have a multi-axis loop, with vars spread across the role that reference tasks of their own, with jinja filters on top of json filters to do something in one task instead of having three tasks to accomplish the same thing. (Please create the three tasks for readability)

- **Controls only do what the control ask for**

  - Our Audit tool and Remediate are intrinsically linked when combined. Things like variables and how the search is executed in our Audit rely on the Remediate being correct when run from the Remediate playbook.
  - Scanners also use the Fix Text and/or intent of the control (sometimes the Fix Text has mistakes...) to check for compliance. If you deviate from this, scanners find false positives.
  - There should be no extra security settings set (even if they are good ideas to set). These roles expect to only set what is defined in the STIG or CIS benchmarks. If other security settings are set, it can cause confusion.

- **Keep it clean**

  - Linting

We use both:

  - ansible-lint
  - yamllint

We also run `pre-commit <https://pre-commit.com>`_ checks on all PRs to ensure this is met in requests.

General Layout
^^^^^^^^^^^^^^

- Users should not have to edit tasks, but vars in ``defaults/main.yml``. Should be used to override settings in the tasks.
  If a control has any variability create a variable for that value
- Follow the specific structure listed in the Layout sections
- For controls that install/uninstall packages please use package module and use ansible_facts.packages in the when where required

  - The package module will use the default package manager for that system, for example ``yum`` (RHEL 7), ``dnf`` (RHEL 8+), ``apt`` (Ubuntu), etc. This allows for a more unified use of tasks between all roles
  - The use of ``ansible_facts.packages`` will skip if it does not need to run and add efficiency to run time

- **Name** ``- name:``

  - Each control gets its own task and that task needs a name. The STIG name format is severity | STIG ID | PATCH or AUDIT | title of control copied from the STIG. The CIS name format is CIS ID | PATCH or AUDIT | title of control copied from CIS.
  - PATCH or AUDIT - This is in reference to the task making a change (PATCH) or not making a change (AUDIT). Tasks that don't make changes are one that
    generally gather information to be used later

- **Block**

  - If there are more than one task to complete a control please keep those in a single task but using a block format.
  - When using blocks the steps should have a pipe ( | ) after the title followed by a description of what that task is doing in the block.

- **Module**

  - This is just the module being used to execute that task, nothing special here

- **Mode**

  - To try and ensure idempotency and the changes to permissions should be X or more restrictive - we use symbolic logic e.g. ``mode: 'u-x,go-wx'``

Variables
^^^^^^^^^

  - ``defaults/main.yml``

    - Any value that can deviate from the example used in the fix text. For example tasks that ask to set permissions X or more restrictive that the permissions value should be a variable
    - Any value that has multiple value options should be a variable
    - These variables should be defined in the ``defaults/main.yml`` file
    - These variables should be formatted as role name followed by the descriptor, rhel10cis_disruption_high for example

  - ``vars/main.yml``

    - While these can be overridden, these will be rare and these are usually set as a default for a value.

- Dynamic Variables (register or set_facts)

  - These are labeled from where/how they are set. This will assist with:

    - reusability across repositories
    - assist in debugging knowing where the value is set

**Naming of variables**

- ``tasks/prelim.yml``

  - These are often used in multiple locations so set in prelim
  - When set here as registered as prelim_description e.g. prelim_apparmor_enforce_status

- ``tasks/*/*.yml``

  - Set by registering output and used within that task
  - descriptive naming e.g. discovered_auditd_conf_files

- **Parameters**

  - When using the ``command`` module to gather information please set ``changed_when``, ``failed_when`` and ``check_mode: false`` accordingly. ``check_mode: false`` causes the task to always run and register, which always creates the registered variable. The action parts of the task that use that var should handle the var if a fail occurred during the ``command`` or ``shell`` function
  - Please always use ``command`` over ``shell``, except when using ( | ) in the command as this will cause issues.
  - When using modules that have aliases, please do not use the alias since those are often not part of the module documentation
  - When using modules that require a path type of parameter please use that first
  - When using modules that regex, please use that second after path where applies

- **Loops**

  - When using loops please use ``loop`` for consistency with the current roles
  - Please use ``loop_control`` on wordy loops
  - Please put the loop list below the ``loop`` like in the example

- **When** - *(Please use when statements on all controls)*

  - The control should have the when set to run when the var for the individual task toggle set to true. Use the toggle named in the role's ``defaults/main/main.yml`` for that control (for example ``rhel8stig_010382`` in RHEL8-STIG, ``rhel_09_171011`` in RHEL9-STIG, ``rhel10cis_rule_6_3_1_2`` in RHEL10-CIS)
  - When you are outside of the block please stack the ``when`` values under the ``when`` call, see example below for clarification.
  - When you are inside of the block you can use a single line for ``when`` and value in a single ``when`` instance. If there are and/or whens please stack those under the when
  - Please do not use empty compares, if you are basing your task run off an empty var please use | length > 0 or | length == 0.

STIG Control Task Layout
^^^^^^^^^^^^^^^^^^^^^^^^

- **Tags**

  - All controls must have tags, but the individual tasks in the block do not get tags. See the example below for clarification
  - The tags are in this order:

    - STIG ID copied from the STIG
    - Category
    - CCI value (NIST group ID)
    - NIST values
    - Security Group ID
    - Rule ID
    - Vulnerability ID
    - Descriptor of what the task is involved with. For example ssh, selinux, pamd, gui, etc. This tag is always lowercase

  - The position of the NIST values differs between roles (RHEL9-STIG and RHEL10-STIG place them after the Vulnerability ID). Follow the role you are working in.

Example from RHEL8-STIG (RHEL-08-010382):

.. code-block:: yaml

    - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel."
      when:
        - rhel8stig_010382
        - rhel8stig_disruption_high
      tags:
        - RHEL-08-010382
        - CAT2
        - CCI-000366
        - NIST800-53R4_CM-6
        - SRG-OS-000480-GPOS-00227
        - SV-237641r1101904_rule
        - V-237641
        - sudo
      block:
        - name: "MEDIUM | RHEL-08-010382 | AUDIT | RHEL 8 must restrict privilege elevation to authorized personnel. | Get ALL settings"
          ansible.builtin.shell: |
            set -o pipefail
            grep -iws 'ALL' /etc/sudoers /etc/sudoers.d/* | cut -d":" -f1 | uniq | sort
          args:
            executable: "{{ rhel8stig_shell_executable }}"
          changed_when: false
          check_mode: false
          failed_when: false
          register: discovered_sudoers_all

        - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel. | Remove format 1"
          when: discovered_sudoers_all.stdout | length > 0
          ansible.builtin.lineinfile:
            path: "{{ item }}"
            regexp: '^\s*ALL\s+ALL\s*=\s*\(ALL\)\s+ALL\s*$'
            state: absent
            validate: '/usr/sbin/visudo -cf %s'
          loop: "{{ discovered_sudoers_all.stdout_lines }}"

        - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel. | Remove format 2"
          when: discovered_sudoers_all.stdout | length > 0
          ansible.builtin.lineinfile:
            path: "{{ item }}"
            regexp: '^\s*ALL\s+ALL\s*=\s*\(ALL:ALL\)\s+ALL\s*$'
            state: absent
            validate: '/usr/sbin/visudo -cf %s'
          loop: "{{ discovered_sudoers_all.stdout_lines }}"

CIS Control Task Layout
^^^^^^^^^^^^^^^^^^^^^^^

- **Tags**

  - All controls must have tags, but the individual tasks in the block do not get tags. See the example below for clarification
  - The tags are in this order:

    - Server Level
    - Workstation Level
    - Automated or Manual, where present. This is from the CIS control in the benchmark documentation and is their assessment of the control being able to be automated or a manual control. If we automate or don't automate the control itself we use the value from the benchmark itself here. Many current tasks no longer carry this tag
    - Patch or Audit. Does the overall task make any changes or just audit/message out
    - Descriptor of what the task is involved with. For example ssh, selinux, pamd, gui, etc. This tag is always lowercase
    - Number of the control. The format is rule_< the number>, rule_6.3.1.2 for example
    - NIST values

  - The relative position of the rule number and NIST values differs between tasks. Follow the role you are working in.

Example from RHEL10-CIS (6.3.1.2):

.. code-block:: yaml

  - name: "6.3.1.2 | PATCH | Ensure auditing for processes that start prior to auditd is enabled"
    when: rhel10cis_rule_6_3_1_2
    tags:
      - level2-server
      - level2-workstation
      - patch
      - auditd
      - grub
      - rule_6.3.1.2
      - NIST800-53R5_AU-12
    block:
      - name: "6.3.1.2 | PATCH | Ensure auditing for processes that start prior to auditd is enabled | Grubby existence of current value"
        ansible.builtin.shell: |
          set -o pipefail
          grubby --info=ALL | grep args | sed -n 's/.*audit=\([[:alnum:]]\+\).*/\1/p'
        args:
          executable: "{{ rhel10cis_shell_executable }}"
        changed_when: false
        failed_when: false
        check_mode: false
        register: discovered_grubby_curr_value_audit_linux

      - name: "6.3.1.2 | PATCH | Ensure auditing for processes that start prior to auditd is enabled | Grubby update, if needed"
        when: discovered_grubby_curr_value_audit_linux.stdout == '' or '0' in discovered_grubby_curr_value_audit_linux.stdout or 'off' in discovered_grubby_curr_value_audit_linux.stdout|lower
        ansible.builtin.command: grubby --update-kernel=ALL --args="audit=1"
        changed_when: true
