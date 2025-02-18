Audit
=====

.. contents::
   :local:
   :backlinks: none

Overview
--------

Ansible remediation for security benchmarks now utilizes an open-source go binary called `goss <https://goss.rocks>`_ to audit the system.

Ensuring consistency in checks by using the same settings and controls
that have been enabled in the remediation steps, are the same ones
checked by the audit.


Considerations
--------------

- The audit runs using the host only compute resources (memory/cpu).
- Please be aware this may have adverse effect running on a heavily utilized system.
- Please consider shared resources when running on many hosts simultaneously.


It can be run in two ways:

- Enabled to run as part of the ansible playbook and is setup to capture pre remediation and post remediation states.
  Using the same configured variables as used in remediation See `Using Audit and Remediate at the same time <../combined/comb-getting-started.html>`_

- Standalone script

  - run_audit.sh (Linux (shell))
  - run_audit.ps1 (Windows(powershell))


Currently Enabled Playbooks
---------------------------

- `CIS Benchmarks <../CIS/CIS_table.html>`_

- `STIG Benchmarks <../STIG/STIG_table.html>`_


Setup auditing as standalone
----------------------------

It is presumed that you have the script downloaded and the audit content ready from
source control or your own configured location.

The following requirements are needed (OS dependant)

- Super user or permissions to run privilege commands

  - Linux sudo can work
  - Windows ability to run security audits and query group or local policy.

- goss binary appropriate for the OS

  - The binary must be accessible by the OS so the scripts can run smoothly with appropriate rights.

    - The expected path for the binary is found inside the relevant OS script and can be adjusted as required.

  - Linux

    - `Binary <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-amd64>`_
    - `Checksum <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-amd64.sha256>`_

  - Windows

    - `Binary <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-alpha-windows-amd64.exe>`_
    - `Checksum <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-alpha-windows-amd64.exe.sha265>`_

.. note::
    The binary only needs to be accessible to the host with ability to use.
    The relevant script needs to be adjust to point to the path of the binary.
    Ensure you have the correct binary for your architecture examples above are AMD64, but also works on ARM64 (may have bad results with auditd settings)

Running the Audit Only as part of remediate playbook
----------------------------------------------------

It is possible to just run the audit on some playbooks (being rolled out across them all). This is a variable set

.. code-block:: yaml

  audit_only: true


This will run the audit based on the same release as the playbook and will then stop.
Extra variables also enable the ability to copy back the audit output to the control node and create a directory structure.

.. code-block:: yaml

  # As part of audit_only
  # This will enable files to be copied back to control node
  fetch_audit_files: false
  # Path to copy the files to will create dir structure
  audit_capture_files_dir: /some/location to copy to on control node


Defining the audit
------------------

Each script runs against a configures variables file found in the content location in

.. code-block:: shell

   {downloaded content}/vars/{benchmark}.yml

These are the variables that configure which controls are run along with some configurable settings during an audit.

Each script has the ability for you to set several variables depending on your environment requirements.
e.g. locations on where to find binary or output locations

There are also switch options to allow you to run a couple of these benchmarks at one time.

Script runtime options

- The group option allows a meta field that can be assigned against the report for use in the analysis if servers are under the same group.

If more than one server group is analyzed, groups can be separated with commas.

- The full audit report has the saved output filename and location information.

Running on Linux
----------------

- Script

  - run_audit.sh (found in content directory)

Understanding variables:

- Uppercase variable are the only ones that should need changing
- lowercase variables are the ones that are discovered or built from existing.

script variables
example:

.. code-block:: shell

   AUDIT_BIN="${AUDIT_BIN:-/usr/local/bin/goss}"  # location of the goss executable
   AUDIT_FILE="${AUDIT_FILE:-goss.yml}"  # the default goss file used by the audit provided by the audit configuration
   AUDIT_CONTENT_LOCATION="${AUDIT_CONTENT_LOCATION:-/var/tmp}"  # Location of the audit configuration file as available to the OS


script help

.. code-block:: shell

   Script to run the goss audit

   Syntax: ./run_audit.sh [-f|-g|-o|-v|-w|-h]
   options:
   -f     optional - change the format output (default value = json)
   -g     optional - Add a group that the server should be grouped with (default value = ungrouped)
   -o     optional - file to output audit data
   -v     optional - relative path to the vars file to load (default e.g. /var/tmp/RHEL7-CIS/vars/CIS.yml)
   -w     optional - Sets the system_type to workstation (Default - Server)
   -h     Print this Help.

   Other options can be assigned in the script itself

**Running goss without script**

This assumes you have goss and access to super user privileges.

It is possible to run goss in its raw form, while this is not recommended, for consistency it is added here.

The script discovers and adds extra inline variablesto the goss output in the form of the metadata fields as found in the goss.yml
This needs to be amended before being able to run in raw form.

- Edit goss.yml remove the lines starting at #metadata and the command tests Vars below

Goss can then be run manually

- full check

.. code-block:: shell

    # {{path to your goss binary}} --vars {{ path to the vars file }} -g {{path to your clone of this repo }}/goss.yml --validate


example:

.. code-block:: shell

    # /usr/local/bin/goss --vars ../vars/cis.yml -g /home/bolly/rh8_cis_goss/goss.yml validate
    ......FF....FF................FF...F..FF.............F........................FSSSS.............FS.F.F.F.F.........FFFFF....

    Failures/Skipped:

    Title: 1.6.1 Ensure core dumps are restricted (Automated)_sysctl
    Command: suid_dumpable_2: exit-status:
    Expected
        <int>: 1
    to equal
        <int>: 0
    Command: suid_dumpable_2: stdout: patterns not found: [fs.suid_dumpable = 0]


    Title: 1.4.2 Ensure filesystem integrity is regularly checked (Automated)
    Service: aidecheck: enabled:
    Expected
        <bool>: false
    to equal
        <bool>: true
    Service: aidecheck: running:
    Expected
        <bool>: false
    to equal
        <bool>: true

    < ---------cut ------- >

    Title: 1.1.22 Ensure sticky bit is set on all world-writable directories
    Command: version: exit-status:
    Expected
        <int>: 0
    to equal
        <int>: 123

    Total Duration: 5.102s
    Count: 124, Failed: 21, Skipped: 5


- running a particular section of tests

.. code-block:: shell

    # /usr/local/bin/goss -g /home/bolly/rh8_cis_goss/section_1/cis_1.1/cis_1.1.22.yml  validate
    ............

    Total Duration: 0.033s
    Count: 12, Failed: 0, Skipped: 0


- changing the output

.. code-block:: shell

    # /usr/local/bin/goss -g /home/bolly/rh8_cis_goss/section_1/cis_1.1/cis_1.1.22.yml  validate -f documentation
    Title: 1.1.20 Check for removeable media nodev
    Command: floppy_nodev: exit-status: matches expectation: [0]
    Command: floppy_nodev: stdout: matches expectation: [OK]
    < -------cut ------- >
    Title: 1.1.20 Check for removeable media noexec
    Command: floppy_noexec: exit-status: matches expectation: [0]
    Command: floppy_noexec: stdout: matches expectation: [OK]


    Total Duration: 0.022s
    Count: 12, Failed: 0, Skipped: 0



Running on Windows
------------------

- Script

  - run_audit.ps1 (found in content directory)

Variables can be set within the script

**Variables for Audit**

.. code-block:: shell

    $DEFAULT_CONTENT_DIR = "C:\remediation_audit_logs"  # This can be changed using cli
    $DEFAULT_AUDIT_BIN = "$DEFAULT_CONTENT_DIR\goss.exe"  # This can be changed using cli option

**script help**

.. code-block:: shell

   NAME
       C:\remediation_audit_logs\Windows-2019-CIS-Audit\run_audit.ps1

   SYNOPSIS
       Wrapper script to run an audit


   SYNTAX
       C:\remediation_audit_logs\Windows-2016-CIS-Audit\run_audit.ps1 [[-auditbin] <String>] [[-auditdir] <String>]
       [[-varsfile] <String>] [[-group] <String>] [[-outfile] <String>] [<CommonParameters>]


   DESCRIPTION
       Wrapper script to run an audit on the system using goss.
       This allows for bespoke variables to be set


   PARAMETERS
       -auditbin <String>

       -auditdir <String>
           default: $DEFAULT_CONTENT_DIR
           Ability to change the location of where the content can be found
           This is where the audit content is stored
           e.g. c:/windows_audit

       -varsfile <String>
           default: $DEFAULT_VARS_FILE
           Ability to set a variable file defined with the settings to match your requirements

       -group <String>
           default: none
           Ability to set a group that the system belongs to
           Can be used when matching similar system in that same group

       -outfile <String>
           default: $AUDIT_CONTENT_DIR\audit_$host_os_hostname_$host_epoch.json
           Ability to set an outfile to send the full audit output to
           Requires path to be set.
           e.g. c:/windows_audit_reports

       <CommonParameters>
           This cmdlet supports the common parameters: Verbose, Debug,
           ErrorAction, ErrorVariable, WarningAction, WarningVariable,
           OutBuffer, PipelineVariable, and OutVariable. For more information, see
           about_CommonParameters (http://go.microsoft.com/fwlink/?LinkID=113216).

       -------------------------- EXAMPLE 1 --------------------------

       PS C:\>./run_audit.ps1

       ./run_audit.ps1 -auditbin c:\path_to\binary.name
       ./run_audit.ps1 -auditdir c:\somepath_for_audit_content
       ./run_audit.ps1 -varsfile myvars.yml
       ./run_audit.ps1 -outfile path\to\audit\output.json
       ./run_audit.ps1 -group webserver
