How to contribute to audit development
--------------------------------------

Adding code
~~~~~~~~~~~

We strive to maintain a set of standards we would like to achieve for all code written.

Considerations
~~~~~~~~~~~~~~

- Keep it as simple as possible to aid investigation and debug.
- Ensure it aligns with the remediate portion **(the remediate and audit repos are intrinsically linked when combined)**.

Layout
~~~~~~

- Each control should be in its own file.
- Use variables wherever possible.
- Related controls may share one file:

  - Multiple stages test (config and running tests)
  - Similar tests (filesystem mount options)

- Structure should be where appropriate

..  code-block:: text

   |- control group e.g. section_1
   |-- grouped controls
   |---- control test

**e.g.**

..  code-block:: text

    |- section_1
    |-- cis_1.1.1.x
    |--- cis_1.1.1.10.yml

    |- cat_1
    |-- RHEL-09-211010.yml

Content
""""""""

- Each task requires the following to be included:

  - Title
  - At least one control variable (whether control ID is to be run or not).

    - If only one test, add the variable before the goss_module itself

  - Use appropriate goss_modules before using command

    - There are circumstances when command allows discovery/filters results

For a full list of goss and how to use the goss_modules (tests).
`Goss Docs <https://goss.readthedocs.io/en/stable/gossfile/#available-tests>`_
(for roles that use Syver, see also `Syver Docs <https://syver.readthedocs.io/en/latest/>`_)

**Example**

*Basic test* (first test from ``section_1/cis_1.1.1.x/cis_1.1.1.10.yml`` in RHEL10-CIS-Audit)

..  code-block:: text

    {{ if .Vars.rhel10cis_level_1 }}
      {{ if .Vars.rhel10cis_rule_1_1_1_10 }}
    command:
      usb-storage:
        title: 1.1.1.10 | Ensure usb-storage kernel module is not available
        exit-status: 0
        exec: "modprobe -n -v usb-storage | grep -E '(usb-storage|install)'"
        stdout:
        - install /bin/true
        meta:
          server: 1
          workstation: 2
          CIS_ID:
          - 1.1.1.10
          NIST800-53R5:
          - CM-7
          - IA-3
          CCI:
          - 000778
          - 001958
          - 003959
      {{ end }}
    {{ end }}


**Breakdown**

..  code-block:: text

    {{ if .Vars.rhel10cis_level_1 }}                                              ## if rhel10cis_level_1 is true
      {{ if .Vars.rhel10cis_rule_1_1_1_10 }}                                      ## if rhel10cis_rule_1_1_1_10 is true
    command:                                                                      ## goss_module
      usb-storage:                                                                ## unique name associated with the command
        title: 1.1.1.10 | Ensure usb-storage kernel module is not available       ## title  {{ control id }} | {{ control title }}
        exit-status: 0                                                            ## Options for goss_module
        exec: "modprobe -n -v usb-storage | grep -E '(usb-storage|install)'"      ## Options for goss_module
        stdout:                                                                   ## Options for goss_module
        - install /bin/true                                                       ## Options for goss_module
        meta:                                                                     ## Meta data used for reporting (see metadata)
          server: 1
          workstation: 2
          CIS_ID:
          - 1.1.1.10
          NIST800-53R5:
          - CM-7
          - IA-3
          CCI:
          - 000778
          - 001958
          - 003959
      {{ end }}                                                                   ## Close if statement
    {{ end }}                                                                     ## Close if statement

**Variable precedence**

Variables should be added higher in the test based on the level of impact.


..  code-block:: text

    {{ .Vars.rhel10cis_section1 }}
      {{ .Vars.rhel10cis_rule_1_1_1_1 }}


Metadata
""""""""

This is added to the audit benchmark for reference across compliance requirements.
There are two levels of metadata:

- **audit metadata** - this is general system information and audit information.
- **control metadata** - this is added to every audit control and is specific to each control.


**Audit Metadata** *(required)*

  - These are items set/discovered about the system within the script set via vars in the script.
  - Referenced in the goss.yml file.

**Contains:**

..  csv-table:: Discovered audit variables
    :header: "Variable Title", "Script variable name", "Purpose"
    :widths: 20, 20, 60

    "host_machine_uuid:", "{{ .Vars.machine_uuid }}", "discovered UUID of system (used as unique identifier)"
    "host_epoch:", "{{ .Vars.epoch }}", "epoch time that script initiated (part of output filename)"
    "host_os_locale:", "{{ .Vars.os_locale }}", "system locale (TZ)"
    "host_os_release:", "{{ .Vars.os_release }}", "OS version (e.g. 7)"
    "host_os_distribution:", "{{ .Vars.os_distribution }}", "OS distribution ( e.g. rhel)"
    "host_hostname:", "{{ .Vars.os_hostname }}", "hostname"
    "host_system_type:", "{{ .Vars.system_type }}"
    " ", "Linux", "Server/Workstation Manually set (default server)"
    " ", "Windows", "Set by -SystemType (default Server)"
    "benchmark_type:", "{{ .Vars.benchmark_type }}", "benchmark type (e.g. CIS)"
    "benchmark_version:", "{{ .Vars.benchmark_version }}", "benchmark version"
    "benchmark_os:", "{{ .Vars.benchmark_os }}", "benchmark OS (e.g. RHEL10)"

**Special Variables**

- **host_automation_group:** {{ .Vars.auto_group }}

  - Used to group like systems when reporting
  - If run via remediate, it uses host group memberships
  - If run via script, it is an optional value or null

**Control Metadata** (required)

  - This consists of data found in the benchmark documentation
  - This potentially changes with each release update (this will need to be correct for the release being worked on)

**CIS Specific**

This contains the following:

- ``server:`` cis level options: (1|2)
- ``workstation:`` cis level: (1|2|NA)
- ``CIS_ID:`` control reference (list)
- Benchmark-dependent mappings:

  - ``NIST800-53R5:`` and ``CCI:`` lists (newer benchmarks, e.g. RHEL10)
  - ``CISv8:`` list plus ``CISv8_IG1``, ``CISv8_IG2``, ``CISv8_IG3`` Booleans (older benchmarks, e.g. RHEL9)

..  code-block:: yaml

    meta:
      server: 1
      workstation: 2
      CIS_ID:
      - 1.1.1.10
      NIST800-53R5:
      - CM-7
      - IA-3
      CCI:
      - 000778
      - 001958
      - 003959

**STIG Specific**

All can be found in the details of the control itself

- ``Cat:`` the category control is associated with either (1|2|3)
- ``CCI:`` Common identifier is found in the STIG documentation
- ``Group_Title:`` list of the SRG groups the control is a part of
- ``NIST800-53R4:`` list of associated NIST controls
- ``Rule_ID:`` changes with every iteration of the control details
- ``STIG_ID:`` control ID known by STIG
- ``Vul_ID:`` vulnerability identifier

..  code-block:: yaml

    meta:
      Cat: 1
      CCI:
      - CCI-000068
      Group_Title:
      - SRG-OS-000033-GPOS-00014
      NIST800-53R4:
      - AC-17
      Rule_ID: SV-258232r1184335_rule
      STIG_ID: RHEL-09-671020
      Vul_ID: V-258232

Gotchas
~~~~~~~

If you have two tasks that refer to the same file or command
(this is currently the unique identifier used in goss),
it will only give you the result of one test (the last one ran).

e.g.

..  code-block:: yaml

   file:
    /etc/selinux/config:
      title: 1.6.1.4 | Ensure the SELinux mode is not disabled | config
      exists: true
      contains:
      - '/^SELINUX( |)=( |)(enforcing|permissive)/'
      - '!/^SELINUX( |)=( |)disabled/'
      meta:
        server: 1
        workstation: 1
        CIS_ID:
        - 1.6.1.4
        CISv8:
        - 3.3
        CISv8_IG1: true
        CISv8_IG2: true
        CISv8_IG3: true

and

..  code-block:: yaml

   file:
    /etc/selinux/config:
      title: 1.6.1.5 | Ensure the SELinux mode is enforcing | config
      exists: true
      contains:
      - '/^SELINUX( |)=( |)enforcing/'
      - '!/^SELINUX( |)=( |)disabled/'
      meta:
        server: 2
        workstation: 2
        CIS_ID:
        - 1.6.1.5
        CISv8:
        - 3.3
        CISv8_IG1: true
        CISv8_IG2: true
        CISv8_IG3: true

**Only one will give you results**
