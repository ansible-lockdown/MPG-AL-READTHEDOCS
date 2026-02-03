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

   goss -g goss.yml -v

Goss is designed to run from the scripts passing discovered variables into Goss for metadata. Without these values being set, Goss will fail. These metadata variables can be seen towards the end of the goss.yml file. Furthermore, the run_audit script shows how these variables are created and passed to Goss.

**Solution:** Always use the provided ``run_audit.sh`` or ``run_audit.ps1`` scripts.

Goss Binary Not Found
^^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   ./run_audit.sh: line XX: /usr/local/bin/goss: No such file or directory

**Solution:**

1. Download the correct binary for your architecture:

   **AMD64/x86_64:**

   .. code-block:: console

      curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-amd64 \
          -o /usr/local/bin/goss
      chmod +x /usr/local/bin/goss

   **ARM64/aarch64:**

   .. code-block:: console

      curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-arm64 \
          -o /usr/local/bin/goss
      chmod +x /usr/local/bin/goss

2. Or update ``AUDIT_BIN`` in the script to point to the correct location.

Exec Format Error
^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   goss: cannot execute binary file: Exec format error

**Cause:** Wrong architecture binary (e.g., x86_64 binary on ARM64 system).

**Solution:**

.. code-block:: console

   # Check your architecture
   uname -m

   # Download the matching binary (see above)

Goss Version Too Old
^^^^^^^^^^^^^^^^^^^^

**Symptom:**

.. code-block:: bash

   WARNING - Goss installed = 0.3.16, does not meet minimum of 0.4.4

**Solution:**

Download and install the latest version:

.. code-block:: console

   curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-amd64 \
       -o /usr/local/bin/goss
   chmod +x /usr/local/bin/goss
   goss --version

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
     "results": [...],
     "summary": {
       "failed-count": 10,
       "test-count": 200,
       "total-duration": 45.2
     }
   }

**Key metrics:**

- **test-count**: Total controls evaluated
- **failed-count**: Controls that failed compliance check
- **skipped-count**: Controls skipped (disabled or not applicable)

Why Are So Many Controls Failing?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Common Causes:**

1. **System not yet remediated** - Run audit after applying hardening
2. **Controls disabled in remediation** - Audit checks all controls by default
3. **Architecture differences** - ARM64 systems have expected auditd failures
4. **Container environment** - Many controls don't apply to containers

**Solution:**

Ensure audit variables match your remediation configuration:

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

On both Windows and Linux, you have the ability to limit the number of processes that run at the same time.

This is set using a variable as part of the playbook:

.. code-block:: yaml

   audit_max_concurrent: 20  # Default is 50

Or if running manually using the run_audit script:

.. code-block:: console

   ./run_audit.sh -m 20

Audit Takes Too Long
^^^^^^^^^^^^^^^^^^^^

**Solutions:**

1. **Reduce concurrent processes:**

   .. code-block:: console

      ./run_audit.sh -m 10

2. **Skip heavy tests** (filesystem scans):

   .. code-block:: yaml

      audit_run_heavy_tests: false

3. **Increase command timeout** for slow systems:

   .. code-block:: yaml

      audit_cmd_timeout: 120000  # milliseconds

Audit Causes High Disk I/O
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some controls scan the entire filesystem. To reduce impact:

1. Run during off-peak hours
2. Disable heavy tests if not required:

   .. code-block:: yaml

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

   Error: vars file not found at /opt/RHEL10-CIS-Audit/vars/CIS.yml

**Solutions:**

1. Verify the audit content is properly extracted:

   .. code-block:: console

      ls -la /opt/RHEL10-CIS-Audit/vars/

2. Specify the vars file path explicitly:

   .. code-block:: console

      ./run_audit.sh -v /path/to/your/vars/CIS.yml

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

3. Run with sudo if required:

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

Set container mode:

.. code-block:: yaml

   is_container: true

See :doc:`Container and Docker Guide </container-guide>` for details.

