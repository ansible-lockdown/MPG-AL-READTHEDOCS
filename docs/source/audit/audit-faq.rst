Audit - FAQ
===========

.. contents::
   :local:
   :backlinks: none

Goss Binary Issues
------------------

Why does goss run manually fail?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example error when running:

.. code-block:: bash

   goss -g goss.yml validate

The audit is designed to run from the scripts, which pass discovered variables into goss or syver for metadata. Without these values being set, the run will fail. These metadata variables can be seen towards the end of the goss.yml file. Furthermore, the run_audit script shows how these variables are created and passed to the binary.

**Solution:** Use the provided ``run_audit.sh`` or ``run_audit.ps1`` scripts. To run the binary directly, see "Running goss without script" in :doc:`Audit </audit/getting-started-audit>`.

Goss Binary Not Found
^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   WARNING - The audit binary is not available at /usr/local/bin/syver
   ## Pre-checks failed please see output

**Solution:**

The roles use `Syver <https://github.com/krameff/syver/releases>`_, a fork of Goss, or on some roles its earlier release under the name `krameff/goss <https://github.com/krameff/goss/releases>`_.
The role's ``audit_bin_url`` and ``audit_bin_version`` defaults show which one and which release it pins, with checksums.
Replace ``<release>`` below with that value, and check the download against the release's ``SHA256SUMS`` file.

1. Download the correct binary for your architecture:

   **AMD64/x86_64:**

   .. code-block:: console

      curl -L https://github.com/krameff/syver/releases/download/<release>/syver-linux-amd64 \
          -o /usr/local/bin/syver
      chmod +x /usr/local/bin/syver

   **ARM64/aarch64:**

   .. code-block:: console

      curl -L https://github.com/krameff/syver/releases/download/<release>/syver-linux-arm64 \
          -o /usr/local/bin/syver
      chmod +x /usr/local/bin/syver

   For roles that pin krameff/goss, use ``https://github.com/krameff/goss/releases/download/<release>/goss-linux-amd64``
   (or ``goss-linux-arm64``) and ``/usr/local/bin/goss``.

2. Or set ``AUDIT_BIN`` (in the script or as an environment variable) to point to the correct location.

Exec Format Error
^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   syver: cannot execute binary file: Exec format error

**Cause:** Wrong architecture binary (e.g., x86_64 binary on ARM64 system).

**Solution:**

.. code-block:: console

   # Check your architecture
   uname -m

   # Download the matching binary (see above)

Goss Version Too Old
^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: text

   WARNING - Audit binary installed = <installed version>, does not meet minimum of <AUDIT_BIN_MIN_VER>

Older goss-based audit repos word this as ``WARNING - Goss installed = ...``.

**Solution:**

Install the release your role pins in ``audit_bin_version.release``:

.. code-block:: console

   curl -L https://github.com/krameff/syver/releases/download/<release>/syver-linux-amd64 \
       -o /usr/local/bin/syver
   chmod +x /usr/local/bin/syver
   syver --version

Architecture-Specific Issues
----------------------------

Why do I have different results between x86_64 and ARM64/aarch64 audits?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ARM64 (aarch64) and x86_64 architectures use different system call numbers and implementations.
This primarily affects auditd-related controls, as ARM64 uses different syscalls for many
file operations (e.g., ``unlinkat`` instead of ``unlink``, ``openat`` instead of ``open``).

**Common causes of ARM64 audit differences:**

- auditd syscall rules reference x86_64-specific syscalls
- Some syscalls don't exist on ARM64
- Kernel module names may differ

**What to expect:**

- Remediation generally works identically on both architectures
- Audit results will show more failures/skips for auditd-related controls on ARM64
- This is expected behavior, not a bug

For detailed information on ARM64 support, workarounds, and best practices, see the
:doc:`ARM64/aarch64 Architecture Guide </arm64-guide>`.

Audit Results and Interpretation
--------------------------------

How Do I Read the Audit Output?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The audit produces JSON output with the following structure:

.. code-block:: json

   {
     "results": [],
     "summary": {
       "failed-count": 10,
       "skipped-count": 5,
       "summary-line": "Count: 200, Failed: 10, Skipped: 5, Duration: 45.200s",
       "test-count": 200,
       "total-duration": 45200000000
     }
   }

**Key metrics:**

- **test-count**: Total tests (assertions) run
- **failed-count**: Tests that failed
- **skipped-count**: Tests skipped
- **total-duration**: Run time in nanoseconds

Why Are So Many Controls Failing?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

1. **System not yet remediated** - Run audit after applying hardening
2. **Controls disabled in remediation** - Audit checks all controls by default
3. **Architecture differences** - ARM64 systems have expected auditd failures
4. **Container environment** - Many controls don't apply to containers

**Solution:**

When running standalone, set the toggles in the audit vars file to match your remediation.
Playbook runs generate this file from the role's variables automatically.

.. code-block:: yaml

   # vars/CIS.yml - should match your remediation settings
   rhel10cis_rule_1_1_1_1: true
   rhel10cis_rule_1_1_1_2: false  # Disabled in remediation

Why Do I Have Failures After Successful Remediation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

1. **Reboot required** - Some changes only take effect after reboot
2. **Service restart needed** - Configuration changes may need service restart
3. **Time-based controls** - Password aging, log rotation need time to apply
4. **Manual controls** - Some controls require manual intervention

**Solution:**

1. Reboot the system after remediation
2. Wait for time-based controls to take effect
3. Review manual control requirements in the benchmark documentation

How Do I Filter Audit Results?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Filter by status:**

.. code-block:: console

   # Show only failures
   cat audit_output.json | jq '.results[] | select(.successful == false)'

   # Show only skipped
   cat audit_output.json | jq '.results[] | select(.skipped == true)'

**Filter by control ID:**

.. code-block:: console

   # Find specific control
   cat audit_output.json | jq '.results[] | select(.title | contains("1.1.1"))'

Performance and Resource Issues
-------------------------------

My system is impacted when running the audit. How can I restrict its effect?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the goss and Syver audits on Linux and Windows, you can limit the number of processes that run at the same time.
The SCC scan in the Windows STIG roles has no equivalent setting.

This is set using a variable as part of the playbook:

.. code-block:: yaml

   audit_max_concurrent: 20  # Default is 50

Or if running manually using the run_audit script:

.. code-block:: console

   # Linux
   ./run_audit.sh -m 20

   # Windows (current Windows CIS audit scripts)
   .\run_audit.ps1 -MaxConcurrent 20

Audit Takes Too Long
^^^^^^^^^^^^^^^^^^^^

**Solutions:**

1. **Reduce concurrent processes:**

   .. code-block:: console

      ./run_audit.sh -m 10

2. **Skip heavy tests** (filesystem scans):

   .. code-block:: yaml

      # Role variable (playbook runs)
      audit_run_heavy_tests: false

      # Standalone: in the audit vars file
      run_heavy_tests: false

3. **Increase command timeout** for slow systems:

   .. code-block:: yaml

      # Role variable (playbook runs)
      audit_cmd_timeout: 120000  # milliseconds

      # Standalone: in the audit vars file
      timeout_ms: 120000

Audit Causes High Disk I/O
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some controls scan the entire filesystem. To reduce impact:

1. Run during off-peak hours
2. Disable heavy tests if not required:

   .. code-block:: yaml

      # Role variable (playbook runs); standalone uses run_heavy_tests in the vars file
      audit_run_heavy_tests: false

3. Consider using ionice on Linux:

   .. code-block:: console

      ionice -c 3 ./run_audit.sh

Script and Configuration Issues
-------------------------------

Variables File Not Found
^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   passed option '-v' /path/to/your/vars/CIS.yml does not exist

**Solutions:**

1. Verify the audit content is properly extracted:

   .. code-block:: console

      ls -la /opt/RHEL10-CIS-Audit/vars/

2. Check the path passed to ``-v`` exists, or omit ``-v`` to use the default ``vars/CIS.yml`` in the content directory:

   .. code-block:: console

      ls -la /path/to/your/vars/CIS.yml

Permission Denied Running Script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   ./run_audit.sh: Permission denied

**Solutions:**

1. Make script executable:

   .. code-block:: console

      chmod +x run_audit.sh

2. Run with bash explicitly:

   .. code-block:: console

      bash run_audit.sh

3. Run as root (the script exits if not run as root):

   .. code-block:: console

      sudo ./run_audit.sh

Output File Not Created
^^^^^^^^^^^^^^^^^^^^^^^

**Symptom:** Audit runs but no output file is created.

**Solutions:**

1. Check output directory permissions:

   .. code-block:: console

      ls -la /opt/  # or your configured output directory

2. Specify output file explicitly:

   .. code-block:: console

      ./run_audit.sh -o /tmp/audit_output.json

3. Check for errors in script execution:

   .. code-block:: console

      ./run_audit.sh 2>&1 | tee audit_debug.log

Container and Special Environments
----------------------------------

Why Do Many Controls Fail in Containers?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Containers lack many components that benchmarks assume exist:

- No systemd (typically)
- No bootloader
- No kernel access
- Limited audit capabilities

**Solution:**

The role detects containers automatically and sets ``system_is_container: true``, loading the
container rule set (``container_vars_file``, default ``is_container.yml``).

See :doc:`Container and Docker Guide </container-guide>` for details.
