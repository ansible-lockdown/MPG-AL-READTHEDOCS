Audit
=====

.. contents::
   :local:
   :backlinks: none

Overview
--------

Ansible Lockdown audits the system with goss, a YAML-based server testing tool written in Go.
The roles use a signed build of Goss: either `krameff/goss <https://github.com/krameff/goss/releases>`_
or its continuation `Syver <https://github.com/krameff/syver/releases>`_.
The role's ``audit_bin_url`` and ``audit_bin_version`` defaults show which one and which release it pins, with checksums.
Both binaries read the same ``goss.yml`` audit content.

The audit uses the same variables and enabled controls as the remediation, so the checks match what was remediated.


Considerations
--------------

- The audit runs using the host only compute resources (memory/cpu).
- Please be aware this may have adverse effect running on a heavily utilized system.
- Please consider shared resources when running on many hosts simultaneously.


It can be run in two ways:

- Enabled to run as part of the Ansible playbook, set up to capture pre remediation and post remediation states
  using the same variables as the remediation. See :doc:`Using Audit and Remediate at the same time </combined/comb-getting-started>`.

- Standalone script

  - run_audit.sh (Linux (shell))
  - run_audit.ps1 (Windows (PowerShell))


Currently Enabled Playbooks
---------------------------

- :doc:`CIS Benchmarks </CIS/CIS_table>`

- :doc:`STIG Benchmarks </STIG/STIG_table>`


Setup auditing as standalone
----------------------------

It is presumed that you have the script downloaded and the audit content ready from
source control or your own configured location.

The following requirements are needed (OS dependent)

- Super user or permissions to run privilege commands

  - Linux sudo can work
  - Windows ability to run security audits and query group or local policy.

- goss or syver binary appropriate for the OS

  - The binary must be accessible by the OS so the scripts can run smoothly with appropriate rights.

    - The expected path for the binary is found inside the relevant OS script and can be adjusted as required.

  - Use the binary and release your role pins in ``audit_bin_url`` and ``audit_bin_version.release``
    (``defaults/main/audit.yml``). Replace ``<release>`` below with that value.

  - Linux

    - Syver: ``https://github.com/krameff/syver/releases/download/<release>/syver-linux-amd64``
    - krameff/goss: ``https://github.com/krameff/goss/releases/download/<release>/goss-linux-amd64``
    - Checksums: the ``syver_<version>_SHA256SUMS`` or ``goss_<version>_SHA256SUMS`` file on the same release page

  - Windows

    - Syver: ``https://github.com/krameff/syver/releases/download/<release>/syver-windows-amd64.exe``
    - Checksums: the ``syver_<version>_SHA256SUMS`` file on the same release page

.. note::
    The binary only needs to be accessible to the host with ability to use.
    The relevant script needs to be adjusted to point to the path of the binary.
    Ensure you have the correct binary for your architecture (examples above are AMD64).

    **ARM64/aarch64 Users:** Download the ARM64 binary (``syver-linux-arm64`` or ``goss-linux-arm64``)
    from the same release page.

    ARM64 audits may show different results for auditd-related controls due to syscall differences.
    See :doc:`ARM64/aarch64 Architecture Guide </arm64-guide>` for details.

Running the Audit Only as part of remediate playbook
----------------------------------------------------

Most current roles can run the audit alone, without remediating. Set:

.. code-block:: yaml

  audit_only: true


This will run the audit based on the same release as the playbook and will then stop.
Extra variables enable copying the audit output back to the control node, or to a location available to the managed node.

.. code-block:: yaml

  # Copy audit output back (fetch) or to another path (copy)
  fetch_audit_output: true
  # fetch or copy
  audit_output_collection_method: fetch
  # Destination for the audit output files
  audit_output_destination: /some/location/on/control/node/


Defining the audit
------------------

Each script runs against a configured variables file found in the content location in

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

Bash Script Explanation: Goss Security Audit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Script

  - run_audit.sh (found in content directory)

This Bash script runs a **security audit** using **goss or syver**.
It is designed to be **Linux OS-agnostic**, configurable, and ensures compliance with
**CIS or STIG** benchmarks.

The excerpts below are from ``run_audit.sh`` in RHEL10-CIS-Audit. Other audit repos follow the same
structure; older goss-based repos default ``AUDIT_BIN`` to ``/usr/local/bin/goss`` with a lower ``AUDIT_BIN_MIN_VER``.

**1. Script Metadata and Change Log**
At the top, the script includes comments detailing changes made over time.
This is useful for **tracking updates, fixes, and enhancements**.

**2. Benchmark and Audit Variables**
Understanding variables:

- Uppercase variables are the only ones that should require changes.
- lowercase variables are the ones that are discovered or built from existing.

.. code-block:: bash

    # Goss benchmark variables (these should not need changing unless new release)
    BENCHMARK=CIS # Benchmark Name aligns to the audit
    BENCHMARK_VER=1.0.1
    BENCHMARK_OS=RHEL10

Defines **benchmark name**, **version**, and **target OS**.

.. code-block:: bash

    # Goss host Variables
    AUDIT_BIN="${AUDIT_BIN:-/usr/local/bin/syver}"  # location of the syver (or goss) executable
    AUDIT_BIN_MIN_VER="0.13.0"
    AUDIT_FILE="${AUDIT_FILE:-goss.yml}"  # the default goss file used by the audit provided by the audit configuration
    AUDIT_CONTENT_LOCATION="${AUDIT_CONTENT_LOCATION:-/opt}"  # Location of the audit configuration file as available to the OS

Defines **audit binary location** and **audit file paths**. ``AUDIT_BIN``, ``AUDIT_FILE`` and
``AUDIT_CONTENT_LOCATION`` can also be set as environment variables.

**3. Help Function**

.. code-block:: bash

    Help()
    {
      # Display Help
      echo "Script to run the syver audit"
      echo
      echo "Syntax: $0 [-f|-g|-m|-o|-v|-w|-h]"
      echo "options:"
      echo "-f     optional - change the format output (options json(default), documentation, rspecish)"
      echo "-g     optional - Add a group that the server should be grouped with (default value = ungrouped)"
      echo "-m     optional - maximum concurrent processes (number, default 50)"
      echo "-o     optional - file to output audit data"
      echo "-v     optional - relative path to the vars file to load (default e.g. $AUDIT_CONTENT_LOCATION/{OS}-$BENCHMARK/vars/$BENCHMARK.yml)"
      echo "-w     optional - Sets the system_type to workstation (Default - Server)"
      echo "-h     Print this Help."
      echo
    }

Displays **usage instructions** when ``-h`` is provided.

**4. Command-Line Arguments Handling**

.. code-block:: bash

    while getopts f:g:m:o:v::wh option; do
      case "${option}" in
        f ) FORMAT=${OPTARG} ;;
        g ) GROUP=${OPTARG} ;;
        m ) MAX=${OPTARG} ;;
        o ) OUTFILE=${OPTARG} ;;
        v ) VARS_PATH=${OPTARG} ;;
        w ) host_system_type=Workstation ;;
        h ) # display Help
          Help
          exit;;
        ? ) # Invalid option
          echo "Invalid option: -${OPTARG}."
          Help
          exit;;
      esac
    done

Uses ``getopts`` to process **command-line arguments**.

**5. Pre-Checks**

.. code-block:: bash

    if [ "$(/usr/bin/id -u)" -ne 0 ]; then
      echo "Script needs to run with root privileges"
      exit 1
    fi

Ensures the script runs with **root privileges**.

**6. Audit Variables and File Paths**

.. code-block:: bash

    audit_content_version=$BENCHMARK_OS-$BENCHMARK-Audit
    audit_content_dir=$AUDIT_CONTENT_LOCATION/$audit_content_version
    audit_vars=vars/${BENCHMARK}.yml

Defines where the audit content and default vars file are expected.

**7. Output File Handling**

.. code-block:: bash

    if [ -z "$OUTFILE" ]; then
      export audit_out=${AUDIT_CONTENT_LOCATION}/audit_${host_os_hostname}-${BENCHMARK}-${BENCHMARK_OS}_${host_epoch}.$format
    else
      export audit_out=${OUTFILE}
    fi

Dynamically sets the output filename based on system details.

**8. Pre-Check for Audit Binary Availability**

.. code-block:: bash

    export FAILURE=0
    if [ -s "${AUDIT_BIN}" ]; then
      echo "OK - Audit binary $AUDIT_BIN is available"
      goss_installed_version="$($AUDIT_BIN -v | awk 'NR==1{print $NF}' | cut -dv -f2)"
      newer_version=$(echo -e "$goss_installed_version\n$AUDIT_BIN_MIN_VER" | sort -V | tail -n 1)
      if [ "$goss_installed_version" = "$newer_version" ] || [ "$goss_installed_version" = "$AUDIT_BIN_MIN_VER" ]; then
        echo "OK - Audit binary is installed and version is ok ($goss_installed_version >= $AUDIT_BIN_MIN_VER)"
      else
        echo "WARNING - Audit binary installed = ${goss_installed_version}, does not meet minimum of ${AUDIT_BIN_MIN_VER}"
        export FAILURE=2
      fi
    else
      echo "WARNING - The audit binary is not available at $AUDIT_BIN "
      export FAILURE=1
    fi

Checks that the **audit binary is installed** and meets the minimum version requirement.
The script also checks that ``goss.yml`` exists in the content directory and stops if any pre-check fails.

**9. Output Format Selection**

.. code-block:: bash

    # defaults
    output_summary="tail -2 $audit_out"
    format_output="-f $format"

    if [ "$format" = json ]; then
       format_output="-f json -o pretty"
       output_summary='grep -A 4 \"summary\": $audit_out'
    elif [ "$format" = junit ] || [ "$format" = tap ]; then
       output_summary=""
    fi

Sets the output format and how the summary is extracted.

**10. Running the Audit**

.. code-block:: bash

    $AUDIT_BIN -g "$audit_content_dir/$AUDIT_FILE" --vars "$varfile_path"  --vars-inline "$audit_json_vars" v --max-concurrent "$max" $format_output > "$audit_out"

Executes the audit with the specified **configuration file**, vars file and discovered metadata.

**11. Displaying the Audit Results**

.. code-block:: bash

    if [ "$(grep -c Count: "$audit_out")" -ge 1 ]  || [ "$format" = junit ] || [ "$format" = tap ]; then
      eval $output_summary
      echo "Completed file can be found at $audit_out"
      echo "###############"
      echo "Audit Completed"
      echo "###############"
    else
      echo -e "Fail: There were issues when running the audit please investigate $audit_out";
      exit 1
    fi

Checks if the audit ran successfully and notifies the user.

.. csv-table:: **Bash Script Summary**
   :header: "Feature", "Description"
   :widths: 10, 25

   "Purpose", "Runs a goss-based OS security audit"
   "Supported OS", "Linux (RHEL, Oracle, etc.)"
   "Customizable", "Output format, grouping and audit file location"
   "Pre-checks", "Ensures script runs as **root** and checks the audit binary"
   "Error Handling", "Alerts for missing files and outdated versions"

**Running goss without script**

This assumes you have goss or syver and access to super user privileges.

It is possible to run the binary in its raw form. While this is not recommended, it is added here for consistency.

The script discovers and adds extra inline variables to the output in the form of the metadata fields as found in the goss.yml.
This needs to be amended before being able to run in raw form.

- Edit goss.yml and remove the ``command: benchmark_meta:`` test at the end of the file (it reads the script-supplied ``.Vars.machine_uuid``, ``.Vars.epoch`` and similar values).

The binary can then be run manually

- full check

.. code-block:: shell

    # {{ path to binary }} -g {{ path to audit content }}/goss.yml --vars {{ path to the vars file }} validate


example (illustrative output):

.. code-block:: shell

    # /usr/local/bin/syver -g ./goss.yml --vars ./vars/CIS.yml validate
    ......FF....FF................FF...F..FF.............F........................FSSSS.............FS.F.F.F.F.........FFFFF....

    Failures/Skipped:

    Title: 1.1.1.10 | Ensure usb-storage kernel module is not available
    Command: usb-storage: exit-status:
    Expected
        <int>: 1
    to equal
        <int>: 0

    < ---------cut ------- >

    Total Duration: 5.102s
    Count: 124, Failed: 21, Skipped: 5


- running a particular section of tests (illustrative output)

.. code-block:: shell

    # /usr/local/bin/syver -g ./section_1/cis_1.1.1.x/cis_1.1.1.10.yml --vars ./vars/CIS.yml validate
    ....

    Total Duration: 0.033s
    Count: 4, Failed: 0, Skipped: 0


- changing the output (illustrative output)

.. code-block:: shell

    # /usr/local/bin/syver -g ./section_1/cis_1.1.1.x/cis_1.1.1.10.yml --vars ./vars/CIS.yml validate -f documentation
    Title: 1.1.1.10 | Ensure usb-storage kernel module is not available
    Command: usb-storage: exit-status: matches expectation: 0
    Command: usb-storage: stdout: matches expectation: ["install /bin/true"]
    < -------cut ------- >

    Total Duration: 0.022s
    Count: 4, Failed: 0, Skipped: 0

Fetch or Copy Audit Files
-------------------------

When ``fetch_audit_output: true``, the role collects the pre and post audit output files after the audit.
``audit_output_collection_method`` selects ``fetch`` (default) or ``copy``, and ``audit_output_destination``
sets where the files go (default ``{{ audit_log_dir }}/audit_summaries/``).

The excerpts below are from ``tasks/fetch_audit_output.yml`` in RHEL10-CIS.

**1. Fetch to Controller**

.. code-block:: yaml

  - name: "POST | FETCH | Fetch files and copy to controller"
    when: audit_output_collection_method == "fetch"
    ansible.builtin.fetch:
      src: "{{ item }}"
      dest: "{{ audit_output_destination }}"
      flat: true
    changed_when: true
    failed_when: false
    register: discovered_audit_fetch_state
    loop:
      - "{{ pre_audit_outfile }}"
      - "{{ post_audit_outfile }}"
    become: false

- **Condition:** Runs only if ``audit_output_collection_method == "fetch"``.
- **Module:** ``fetch`` copies files **from the managed node to the Ansible controller**.
- **src:** Points to the audit output file on the managed node.
- **dest:** Directory on the controller where files are saved.
- **flat:** Prevents creating full directory paths under ``dest``.
- **changed_when:** Always reports changed.
- **failed_when:** Prevents task failure if the file doesn't exist.
- **register:** Stores the result in ``discovered_audit_fetch_state``.
- **loop:** Iterates over both ``pre_audit_outfile`` and ``post_audit_outfile``.
- **become:** ``false`` indicates no privilege escalation is used.

**2. Copy Method**

.. code-block:: yaml

  - name: "POST | FETCH | Copy files to location available to managed node"
    when: audit_output_collection_method == "copy"
    ansible.builtin.copy:
      src: "{{ item }}"
      dest: "{{ audit_output_destination }}"
      mode: 'u-x,go-wx'
      flat: true
    failed_when: false
    register: discovered_audit_copy_state
    loop:
      - "{{ pre_audit_outfile }}"
      - "{{ post_audit_outfile }}"

- **Condition:** Runs if ``audit_output_collection_method == "copy"``.
- **Module:** ``copy`` without ``remote_src``, so in the current task ``src`` is read from the controller, not the managed node.
- **mode:** Removes execute for everyone and write for group and other (for example ``rw-r--r--``).
- **failed_when:** Prevents task failure if the copy does not succeed.
- **register:** Stores result in ``discovered_audit_copy_state``.

**3. Show Warning if Fetch/Copy Fails**

.. code-block:: yaml

  - name: "POST | FETCH | Fetch files and copy to controller | Warning if issues with fetch_audit_files"
    when:
      - (audit_output_collection_method == "fetch" and not discovered_audit_fetch_state.changed) or
        (audit_output_collection_method == "copy" and not discovered_audit_copy_state.changed)
    block:
      - name: "POST | FETCH | Fetch files and copy to controller | Warning if issues with fetch_audit_files"
        ansible.builtin.debug:
          msg: "Warning!! Unable to write to localhost {{ audit_output_destination }} for audit file copy"

      - name: "POST | FETCH | Fetch files and copy to controller | Warning if issues with fetch_audit_files"
        ansible.builtin.import_tasks:
          file: warning_facts.yml
        vars:
          warn_control_id: "FETCH_AUDIT_FILES"

- **Purpose:** Emits a warning and records it in the role's warning count if no files were transferred.
- **Condition:** Based on whether the transfer task reported a change. Because the fetch task always reports changed, this warning fires only for the ``copy`` method.
- **Message:** Informs the user that the output destination couldn't be written to.

.. csv-table:: **Audit Fetch vs Copy Summary Table**
   :header: "Feature", "Description", "Condition"
   :widths: 10, 15, 20

   "Fetch files to controller", "Copies files to control node using ``fetch``", "audit_output_collection_method == 'fetch'"
   "Copy files", "Uses ``copy``; ``src`` is read from the controller in the current task", "audit_output_collection_method == 'copy'"
   "Error Handling", "Displays a warning if the copy reports no change", "Based on fetch/copy result ``changed`` status"


Running on Windows
------------------

PowerShell Script Explanation: Goss Security Audit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Script

  - run_audit.ps1 (found in content directory)

This PowerShell script serves as a wrapper to run an audit on a system using syver.
The description below is from ``run_audit.ps1`` in Windows-2022-CIS-Audit; Windows-2025-CIS-Audit and
Windows-11-CIS-Audit use the same parameters.
The legacy Windows-2016-CIS-Audit and Windows-2019-CIS-Audit scripts differ: they use goss and the parameters
``-auditbin``, ``-auditdir``, ``-varsfile``, ``-group`` and ``-outfile``.

**Parameters**

The script supports the following parameters:

- **Format** (default: ``json``):
    - Output format: ``json``, ``documentation``, ``rspecish``, ``junit``, ``tap``, ``nagios`` or ``silent``.

- **Group** (default: ``ungrouped``):
    - Used to categorize the system into a specific group for comparison.

- **MaxConcurrent** (default: ``50``):
    - Maximum number of tests run at the same time.

- **OutFile** (default: ``<AUDIT_CONTENT_LOCATION>\audit_<hostname>-<benchmark>-<benchmark OS>_<epoch>.<format>``):
    - Defines the output file path for storing the full audit results.

- **VarsPath** (default: ``<audit content dir>\vars\CIS.yml``):
    - Allows specifying a variables file containing settings for the audit.

- **SystemType** (default: ``Server``):
    - ``Server`` or ``Workstation``.

- **CollectOnly** (switch):
    - Collects the policy snapshot and stops.

- **SkipCollect** (switch):
    - Reuses an existing policy snapshot instead of collecting a new one.

The binary and content locations are set with environment variables:

- ``AUDIT_BIN`` (default ``C:\Program Files\syver\syver.exe``)
- ``AUDIT_FILE`` (default ``goss.yml``)
- ``AUDIT_CONTENT_LOCATION`` (default ``%ProgramData%``); the content is expected in ``<AUDIT_CONTENT_LOCATION>\<benchmark OS>-<benchmark>-Audit``

**Usage Examples**

.. code-block:: console

    # Run the script with default settings
    .\run_audit.ps1

    # Specify a custom path for the audit binary
    $env:AUDIT_BIN = 'C:\path_to\syver.exe'; .\run_audit.ps1

    # Define a custom audit content location
    $env:AUDIT_CONTENT_LOCATION = 'C:\somepath_for_audit_content'; .\run_audit.ps1

    # Use a specific variables file
    .\run_audit.ps1 -VarsPath C:\path\myvars.yml

    # Set a custom output file path
    .\run_audit.ps1 -OutFile C:\audit\output.json

    # Assign the system to a group and limit concurrency
    .\run_audit.ps1 -Group webserver -MaxConcurrent 20

**Script Functionality**

**1. Define Default Values**
  The script sets default values for:
    - The benchmark type, version and OS (for example ``CIS``, ``4.0.0``, ``Windows-2022``).
    - The audit binary, audit file and content location.

**2. Identify Server Role**
  Using ``Get-CimInstance Win32_ComputerSystem`` (DomainRole), the script classifies the host as:
    - Domain Controller
    - Member Server
    - Standalone

  CIS treats any server that is not a domain controller as a Member Server.

**3. Validate Prerequisites**
  The script checks that it runs with Administrator privileges, that the audit binary is present and meets the
  minimum version, and that ``goss.yml`` and the vars file exist. If any check fails, it reports a warning and exits.

**4. Collect Policy Snapshot**
  The script runs ``secedit`` (account policy and user rights) and ``auditpol`` once each and writes a policy
  snapshot under ``%SystemRoot%\Temp``. What to collect comes from ``collector_targets.json``.
  The audit checks against this snapshot.

**5. Collect System Metadata**
  The script gathers system information such as:
    - Machine UUID
    - OS Version and Build
    - Time zone
    - Hostname
    - Epoch time for timestamping output files

**6. Execute the Audit**
  The script runs syver with ``--use-alpha=1`` (required on Windows), passing the metadata as a second ``--vars``
  file, and stores the results in the specified output file.

**7. Output Summary**
  The script prints the summary for ``json`` and ``rspecish`` output, or the last two lines for ``documentation``,
  followed by the output file location.

.. csv-table:: **PowerShell Script Summary**
   :header: "Feature", "Description"
   :widths: 15, 30

   "Purpose", "Runs a goss-based OS security audit per parameters"
   "Host roles detected", "Domain Controller, Member Server, Standalone"
   "Collect System Metadata", "OS Version, Hostname, Epoch time"
   "Pre-checks", "Verifies Administrator rights, the audit binary and version, and the content and vars files"
   "Error Handling", "Alerts for missing files and vars"
