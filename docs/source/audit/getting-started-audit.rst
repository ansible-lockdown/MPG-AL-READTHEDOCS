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

===============================
Bash Script Explanation: Goss Security Audit
===============================

- Script

  - run_audit.sh (found in content directory)

This Bash script runs a **security audit** using **Goss**, a YAML-based testing framework.
It is designed to be **Linux OS-agnostic**, configurable, and ensures compliance with
**CIS or STIG** benchmarks.


**1. Script Metadata and Change Log**

At the top, the script includes comments detailing changes made over time.
This is useful for **tracking updates, fixes, and enhancements**.

**2. Benchmark and Audit Variables**

Understanding variables:

- Uppercase variable are the only ones that should need changing
- lowercase variables are the ones that are discovered or built from existing.

.. code-block:: bash

    # Goss benchmark variables (these should not need changing unless new release)
    BENCHMARK=CIS  # Benchmark Name aligns to the audit
    BENCHMARK_VER=1.0.0
    BENCHMARK_OS=RHEL9

Defines **benchmark name**, **version**, and **target OS**.

.. code-block:: bash

    # Goss host Variables
    AUDIT_BIN="${AUDIT_BIN:-/usr/local/bin/goss}"  # location of the goss executable
    AUDIT_BIN_MIN_VER="0.4.4"
    AUDIT_FILE="${AUDIT_FILE:-goss.yml}"  # default Goss configuration file
    AUDIT_CONTENT_LOCATION="${AUDIT_CONTENT_LOCATION:-/opt}"  # Location for audit files

Defines **Goss binary location** and **audit file paths**.

**3. Help Function**

.. code-block:: bash

    Help()
    {
      echo "Script to run the goss audit"
      echo "Syntax: $0 [-f|-g|-o|-v|-w|-h]"
      echo "options:"
      echo "-f     optional - change the format output (default value = json)"
      echo "-g     optional - Add a group that the server should be grouped with"
      echo "-o     optional - file to output audit data"
      echo "-v     optional - relative path to the vars file"
      echo "-w     optional - Sets the system_type to workstation"
      echo "-h     Print this Help."
    }

Displays **usage instructions** when `-h` is provided.

**4. Command-Line Arguments Handling**

.. code-block:: bash

    while getopts f:g:o:v::wh option; do
      case "${option}" in
        f ) FORMAT=${OPTARG} ;;  # Output format (json, rspecish, etc.)
        g ) GROUP=${OPTARG} ;;   # Defines server group
        o ) OUTFILE=${OPTARG} ;; # Specifies output file
        v ) VARS_PATH=${OPTARG} ;; # Variables file path
        w ) host_system_type=Workstation ;; # Change system type to Workstation
        h ) Help; exit;; # Show help and exit
        ? ) echo "Invalid option: -${OPTARG}."; Help; exit;; # Invalid option handler
      esac
    done

Uses `getopts` to process **command-line arguments**.

**5. Pre-Checks**

.. code-block:: bash

    if [ "$(/usr/bin/id -u)" -ne 0 ]; then
      echo "Script needs to run with root privileges"
      exit 1
    fi

Ensures the script runs with **root privileges**.

.. code-block:: bash

    if [ "$(grep -Ec "rhel|oracle" /etc/os-release)" != 0 ]; then
      os_vendor="RHEL"
    else
      os_vendor="$(hostnamectl | grep Oper | cut -d : -f2 | awk '{print $1}' | tr '[:lower:]')"
    fi

Detects the **OS vendor**.

**6. Audit Variables and File Paths**

.. code-block:: bash

    audit_content_version=$os_vendor$os_maj_ver-$BENCHMARK-Audit
    audit_content_dir=$AUDIT_CONTENT_LOCATION/$audit_content_version
    audit_vars=vars/${BENCHMARK}.yml

Defines paths for **storing audit results**.

**7. Output File Handling**

.. code-block:: bash

    if [ -z "$OUTFILE" ]; then
      export audit_out=${AUDIT_CONTENT_LOCATION}/audit_${host_os_hostname}-${BENCHMARK}-${BENCHMARK_OS}_${host_epoch}.$format
    else
      export audit_out=${OUTFILE}
    fi

Dynamically sets the output filename based on system details.

**8. Pre-Check for Goss Availability**

.. code-block:: bash

    if [ -s "${AUDIT_BIN}" ]; then
      goss_installed_version="$($AUDIT_BIN -v | awk '{print $NF}' | cut -dv -f2)"
      newer_version=$(echo -e "$goss_installed_version\n$AUDIT_BIN_MIN_VER" | sort -V | tail -n 1)
      if [ "$goss_installed_version" = "$newer_version" ] || [ "$goss_installed_version" = "$AUDIT_BIN_MIN_VER" ]; then
        echo "OK - Goss is installed and version is ok ($goss_installed_version >= $AUDIT_BIN_MIN_VER)"
      else
        echo "WARNING - Goss installed = ${goss_installed_version}, does not meet minimum of ${AUDIT_BIN_MIN_VER}"
        export FAILURE=2
      fi
    else
      echo "WARNING - The audit binary is not available at $AUDIT_BIN"
      export FAILURE=1
    fi

Checks if **Goss is installed** and meets the minimum version requirement.

**9. Running the Audit**

.. code-block:: bash

    echo "Audit Started"
    $AUDIT_BIN -g "$audit_content_dir/$AUDIT_FILE" --vars "$varfile_path" --vars-inline "$audit_json_vars" v $format_output > "$audit_out"

Executes the **Goss audit** with the specified **configuration file**.

**10. Displaying the Audit Results**

.. code-block:: bash

    output_summary="tail -2 $audit_out"
    format_output="-f $format"

    if [ "$format" = json ]; then
       format_output="-f json -o pretty"
       output_summary='grep -A 4 \"summary\": $audit_out'
    elif [ "$format" = junit ] || [ "$format" = tap ]; then
       output_summary=""
    fi

Formats and extracts audit results based on the selected output format.

.. code-block:: bash

    if [ "$(grep -c $BENCHMARK "$audit_out")" != 0 ] || [ "$format" = junit ] || [ "$format" = tap ]; then
      eval $output_summary
      echo "Completed file can be found at $audit_out"
      echo "Audit Completed"
    else
      echo -e "Fail: There were issues when running the audit, please investigate $audit_out"
    fi

Checks if the audit ran successfully and notifies the user.

.. csv-table:: *Summary*
   :header: "Feature", "Description"
   :widths: 15, 25

   "Purpose", "Runs a Goss-based security audit"
   "Supported OS", "Linux (RHEL, Oracle, etc.)"
   "Customizable", "Output format, grouping, audit file location"
   "Pre-checks", "Ensures script runs as **root**, checks Goss"
   "Error Handling", "Alerts for missing files, outdated versions"

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

===============================
PowerShell Script Explanation: Goss Security Audit
===============================

- Script

  - run_audit.ps1 (found in content directory)

Variables can be set within the script

This PowerShell script serves as a wrapper to run an audit on a system using `goss`.
It allows users to set custom variables for the audit, including paths for the audit
content, binary, and output files.

**Parameters**

The script supports the following parameters:

- **auditdir** (default: `$DEFAULT_CONTENT_DIR`):
  Specifies the location where the audit content is stored (e.g., `C:\\windows_audit`).

- **binpath** (default: `$DEFAULT_AUDIT_BIN`):
  Defines the path to the audit binary (e.g., `C:\\$DEFAULT_CONTENT_DIR\goss.exe`).

- **varsfile** (default: `$DEFAULT_VARS_FILE`):
  Allows specifying a variable file containing settings for the audit.

- **group** (default: `none`):
  Used to categorize the system into a specific group for comparison.

- **outfile** (default: `$AUDIT_CONTENT_DIR\\audit_$host_os_hostname_$host_epoch.json`):
  Defines the output file path for storing the full audit results.

**Usage Examples**

Run the script with default settings:

.. code-block:: shell
.\run_audit.ps1


Specify a custom path for the audit binary:

.. code-block:: shell
.\run_audit.ps1 -auditbin C:\path_to\binary.exe


Define a custom audit directory:

.. code-block:: shell
.\run_audit.ps1 -auditdir C:\somepath_for_audit_content


Use a specific variables file:

.. code-block:: shell
.\run_audit.ps1 -varsfile myvars.yml

Set a custom output file path:

.. code-block:: shell
.\run_audit.ps1 -outfile C:\audit\output.json

Assign the system to a group:

.. code-block:: shell
.\run_audit.ps1 -group webserver

**Script Functionality**

**1. Define Default Values**
   The script sets default values for:
   - The benchmark type (`CIS or STIG`).
   - The Windows version (`Windows 20XX`).
   - The default content directory, audit binary path, and variable file.

**2. Validate File Paths**
   The script verifies the existence of essential files, such as the audit binary and content files. If any file is missing, it displays a warning and exits.

**3. Identify Server Type**
   Using `wmic.exe`, the script determines the server role, which could be:
   - Standalone Server
   - Member Server
   - Primary Domain Controller (PDC)
   - Backup Domain Controller (BDC)
   - Workstation

**4. Collect System Metadata**
   The script gathers system information such as:
   - Machine UUID
   - OS Version & Locale
   - Hostname
   - Epoch time for timestamping output files

**5. Run System Audit Commands**
   Depending on the server type, the script executes:
   - `auditpol.exe` to capture audit policies.
   - `secedit.exe` for security configuration exports (on standalone servers).
   - `gpresult.exe` for Group Policy results (on domain-connected machines).

**6. Generate JSON Metadata**
   The script constructs a JSON object containing system metadata for the audit.

**7. Execute the Audit**
   The script runs the `goss` audit using the collected metadata, storing the results in the specified output file.

**8. Output Summary**
   The script summarizes the audit results:
   - If successful, it displays the last few lines of the audit report.
   - If failed, it prompts the user to investigate.
