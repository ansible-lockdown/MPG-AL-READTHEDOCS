How to contribute to remediate development
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
  - For example if you have a multi-axis loop, with vars spread across the role that reference tasks of their own, with jinja filters on top of json filters
  to do something in one task instead of having three tasks to accomplish the same thing. (Please create the three tasks for readability)

- **Controls only do what the control ask for**
  - Our Audit tool and Remediate are intrinsically linked when combined. Things like variables and how the search is executed in our Audit rely on the Remediate being correct when run from the Remediate playbook.
  - Scanners also use the Fix Text and/or intent of the control (sometimes the Fix Text has mistakes...) to check for compliance. If you deviate from this, scanners find false positives.
  - There should be no extra security settings set (even if they are good ideas to set). These roles expect to only set what is defined in the STIG or CIS benchmarks. If other security settings are set, it can cause confusion.

Remediate Code Layout
~~~~~~~~~~~~~~~~~~~~~

General Layout
^^^^^^^^^^^^^^

- Each control should be it's own task. If it needs to be multiple tasks create a block for those tasks, see example in the Layout sections
- Users should not have to edit tasks, but vars in ``defaults/main.yml``. If a control has any variability create a variable for that value
- Follow the structure listed in the Layout sections
- For controls that install/uninstall packages please use package module and use ansible_facts.packages in the when

  - The package module will use the default package manager for that system, for example yum (RHEL 7), dnf (RHEL 8+), apt (Ubuntu), etc. This allows for a more unified use of tasks between all roles
  - The use of ansible_facts.packages will skip if it does not need to run and add efficiency to run time

STIG Control Task Layout
^^^^^^^^^^^^^^^^^^^^^^^^

- **Name** ``- name:``
  - Each control gets it's own task and that task needs a name. The name format is category | STIG ID | PATCH or AUDIT | title of control copied from STIG.
  - PATCH or AUDIT - This is in reference to the task making a change (PATCH) or not making a change (AUDIT). Tasks that don't make changes are one that
    generally gather information to be used later

- **Block**
  - If there are more than one task to complete a control please keep those in a single task but using a block format.
  - When using blocks the steps should have a pipe ( | ) after the title followed by a description of what that task is doing in the block.

- **Module**
  - This is just the module being used to execute that task, nothing special here

- **Parameters**
  - When using the ``shell`` module to gather information please set ``changed_when`` and ``failed_when`` to false. This will cause the task to always
  run and register which always creates the variable registering. The action parts of the task that use that var should handle the var if a fail occurred
  during the ``command`` or ``shell`` function
  - Please always use ``shell`` over ``command``. The ``command`` module is being phased out, but also for consistency please use ``shell``
  - When using modules that have alias's, please do not use the alias since those are often not part of the module documentation
  - When using modules that require a path type of parameter please use that first
  - When using modules that regex, please use that second after path where applies

- **Registers**
  - Please adhere to the exiting format of registered variable names
  - Dynamic variables are variables set in-line of a task, rhel_08_010382_sudoers_all in the example below. Please follow the all lower case using underscores
  instead of dashes STIG ID followed by a descriptive name. This helps keep variable names from overlapping in this role or other playbooks/collections you use this role with.

- **Variables**
  - Any value that can deviate from the example used in the STIG fix text. For example tasks that ask to set permissions X or more restrictive that the permissions value should be a variable
  - Any value that has multiple value options should be a variable
  - These variables should be defined in the ``defaults/main.yml`` file
  - These variables should be formatted as role name followed by the descriptor, rhel8stig_disruption_high for example

- **With_items**
  - When using loops please use with_items for consistency. We know ``loop`` has much of the same functionality as ``with_items`` but for consistency we would like ``with_items`` since it covers all uses
  - Please use ``loop_control`` on wordy loops
  - Please put the loop list below the ``with_items`` like in the example

- **When** - *(Please use when statements on all controls)*
  - The control should have the when set to run when the var for the individual task toggle set to true. That toggle is the STIG ID, all lower case with underscores instead of dashes
  - When you are outside of the block please stack the ``when`` values under the ``when`` call, see example below for clarification.
  - When you are inside of the block you can use use single line for ``when`` and value in a single ``when`` instance. If there are and/or whens please stack those under the when
  - Please do not use empty compares, if you are basing your task run off an empty var please use | length > 0 or | length == 0.

- **Tags**
  - All controls must have tags, but the individual tasks in the block do not get tags. See the example below for clarification
  - The tags are in this specific order:
    - STIG ID copied from the STIG
    - Category
    - CCI value (NIST group ID)
    - Security Group ID
    - Rule ID
    - Vulnerability ID
    - Descriptor of what the task is involved with. For example ssh, selinux, pamd, gui, etc. This tag is always lowercase

.. code-block:: yaml

    - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel."
      block:
          - name: "MEDIUM | RHEL-08-010382 | AUDIT | RHEL 8 must restrict privilege elevation to authorized personnel. | Get ALL settings"
            ansible.builtin.shell: grep -iws 'ALL' /etc/sudoers /etc/sudoers.d/* | cut -d":" -f1 | uniq | sort
            changed_when: false
            failed_when: false
            register: rhel_08_010382_sudoers_all

          - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel. | Remove format 1"
            ansible.builtin.lineinfile:
                path: "{{ item }}"
                regexp: 'ALL ALL=(ALL) ALL'
                state: absent
                validate: '/usr/sbin/visudo -cf %s'
            with_items:
                - "{{ rhel_08_010382_sudoers_all.stdout_lines }}"
            when: rhel_08_010382_sudoers_all.stdout | length > 0

          - name: "MEDIUM | RHEL-08-010382 | PATCH | RHEL 8 must restrict privilege elevation to authorized personnel. | Remove format 2"
            ansible.builtin.lineinfile:
                path: "{{ item }}"
                regexp: 'ALL ALL=(ALL:ALL) ALL'
                state: absent
                validate: '/usr/sbin/visudo -cf %s'
            with_items:
                - "{{ rhel_08_010382_sudoers_all.stdout_lines }}"
            when: rhel_08_010382_sudoers_all.stdout | length > 0
      when:
          - rhel_08_010382
          - rhel8stig_disruption_high
      tags:
          - RHEL-08-010382
          - CAT2
          - CCI-000366
          - SRG-OS-000480-GPOS-00227
          - SV-237641r646893_rule
          - V-237641
          - sudo


CIS Control Task Layout
^^^^^^^^^^^^^^^^^^^^^^^

- **Name** ``- name:``
  - Each control gets it's own task and that task gets a name. The name format is Control Number | PATCH or AUDIT | Title copied from CIS control

- **Block**
  - If there is more than one task to complete a control please those in a single task but using a block format, example below.
  - When using blocks the steps should have a pipe ( | ) after the title followed by a description of what that task is doing in the block.

- **Module**
  - This is just the module being used to execute that task, nothing special here

- **Parameters**
  - When using the ``shell`` module to gather information please set ``changed_when`` and ``failed_when`` to false. This will cause the task to
  always run and register which always creates the variable registering. The action parts of the task that use that var should handle the var if a
  fail occurred during the ``command`` or ``shell`` function
    - Please always use ``shell`` over ``command``. The ``command`` module is being phased out, but also for consistency please use ``shell``
  - When using modules that have alias's, please do not use the alias since those are often not part of the module documentation
  - When using modules that require a path type of parameter please use that first
  - When using modules that regex, please use that second after path where applies

- **Registers**
  - Please adhere to the exiting format of registered variable names
  - Dynamic variables are variables set in-line of a task, rhel8cis_4_1_1_1_3_grub_cmdline_linux in the example below. Please follow the all lower
  case standard using underscores instead of periods/dots with benchmark name followed by the CIS control number and finally a descriptive name.
  This helps keep variable names from overlapping in this role or other playbooks/collections you use this role with.

- **Variables**
  - Any value that can deviate from the example used in the STIG fix text. For example tasks that ask to set permissions X or more restrictive that the permissions value should be a variable
  - Any value that has multiple value options should be a variable
  - These variables should be defined in the ``defaults/main.yml`` file
  - These variables should be formatted as role name followed by the descriptor, rhel8stig_disruption_high for example

- **With_items**
  - When using loops please use with_items for consistency. We know ``loop`` has much of the same functionality as ``with_items`` but for consistency we would like ``with_items``
since it covers all uses
  - Please use ``loop_control`` on wordy loops
  - Please put the loop list below the ``with_items`` like in the example

- **When** - *(Please use when statements on all controls)*
  - The control should have the when set to run when the var for the individual task toggle set to true. That toggle is the STIG ID, all lower case with underscores instead of dashes
  - When you are outside of the block please stack the ``when`` values under the ``when`` call, see example below for clarification.
  - When you are inside of the block you can use use single line for ``when`` and value in a single ``when`` instance. If there are and/or whens please stack those under the when
  - Please do not use empty compares, if you are basing your task run off an empty var please use | length > 0 or | length == 0.

- **Tags**
  - All controls must have tags, but the individual tasks in the block do not get tags. See the example below for clarification
  - The tags are in this specific order:

    - Server Level
    - Workstation Level
    - Automated or Manual. This is from the CIS control in the benchmark documentation and is their assessment of the control being able to be automated or a manual control.
    If we automate or don't automate the control itself we use the value from the benchmark itself here
    - Patch or Audit. Does the overall task make any changes or just audit/message out
    - Descriptor of what the task is involved with. For example ssh, selinux, pamd, gui, etc. This tag is always lowercase
    - Number of the control. The format is rule_< the number>, rule_4.1.1.3 for example

.. code-block:: yaml

  - name: "4.1.1.3 | PATCH | Ensure auditing for processes that start prior to auditd is enabled"
    block:
        - name: "4.1.1.3 | AUDIT | Ensure auditing for processes that start prior to auditd is enabled | Get GRUB_CMDLINE_LINUX"
          ansible.builtin.shell: grep 'GRUB_CMDLINE_LINUX=' /etc/default/grub | sed 's/.$//'
          changed_when: false
          failed_when: false
          check_mode: no
          register: rhel8cis_4_1_1_3_grub_cmdline_linux

        - name: "4.1.1.3 | PATCH | Ensure auditing for processes that start prior to auditd is enabled | Replace existing setting"
          ansible.builtin.replace:
              path: /etc/default/grub
              regexp: 'audit=.'
              replace: 'audit=1'
          notify: grub2cfg
          when: "'audit=' in rhel8cis_4_1_1_3_grub_cmdline_linux.stdout"

        - name: "4.1.1.3 | PATCH | Ensure auditing for processes that start prior to auditd is enabled | Add audit setting if missing"
          ansible.builtin.lineinfile:
              path: /etc/default/grub
              regexp: '^GRUB_CMDLINE_LINUX='
              line: '{{ rhel8cis_4_1_1_3_grub_cmdline_linux.stdout }} audit=1"'
          notify: grub2cfg
          when: "'audit=' not in rhel8cis_4_1_1_3_grub_cmdline_linux.stdout"
    when:
        - rhel8cis_rule_4_1_1_3
    tags:
        - level2-server
        - level2-workstation
        - automated
        - patch
        - auditd
        - grub
        - rule_4.1.1.3
