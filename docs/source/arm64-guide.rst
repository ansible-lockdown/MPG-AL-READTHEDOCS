ARM64/aarch64 Architecture Guide
=================================

.. contents::
   :local:
   :backlinks: none

Overview
--------

With the growing adoption of ARM64 (aarch64) processors in servers, cloud instances, and edge computing, Ansible Lockdown has extended support
for hardening ARM-based systems.

.. important::

   Security benchmarks from CIS and DISA STIG are primarily designed and tested for x86_64
   architecture. ARM64 support is provided on a best-effort basis and is not officially
   covered by the benchmark providers.

Support Status
--------------

**Remediation:**
ARM64 remediation is generally well-supported. Most Ansible tasks are architecture-agnostic
and work identically on ARM64 systems.

**Audit:**
ARM64 audit support has specific limitations, particularly around auditd system calls.
See `Known Limitations`_ for details.

   Windows ARM64 is not currently supported by the Ansible Lockdown roles.

Getting Started on ARM64
------------------------

Prerequisites
~~~~~~~~~~~~~

1. **Verify Architecture:**

.. code-block:: console

   uname -m
   # Expected output: aarch64

2. **Download ARM64 Goss Binary:**

For audit functionality, download the ARM64 version of the Goss binary:

- `Goss ARM64 Binary <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-arm64>`_
- `Goss ARM64 Checksum <https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-arm64.sha256>`_

.. code-block:: console

   # Download and install Goss for ARM64
   curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-arm64 \
       -o /usr/local/bin/goss
   chmod +x /usr/local/bin/goss

   # Verify installation
   goss --version

3. **Configure Audit Script:**

Update the ``run_audit.sh`` script to use the ARM64 binary path if different from default.

Running Remediation
~~~~~~~~~~~~~~~~~~~

Remediation works the same on ARM64 as x86_64:

.. code-block:: console

   ansible-playbook -i inventory site.yml

No special configuration is needed for most controls.

Running Audit
~~~~~~~~~~~~~

.. code-block:: console

   # Run audit with ARM64 binary
   AUDIT_BIN=/usr/local/bin/goss ./run_audit.sh

Known Limitations
-----------------

auditd System Call Differences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most significant limitation on ARM64 relates to the Linux audit subsystem (auditd).
ARM64 and x86_64 use different system call numbers and some system calls have different
names or don't exist on ARM64.

**Impact:**

- Audit rules monitoring specific syscalls may not work correctly
- Some audit tests will fail or be skipped
- False positives/negatives in compliance reports

**Affected Controls:**

CIS and STIG benchmarks with auditd rules for the following are affected:
- File access monitoring (open, creat, unlink syscalls)
- Privileged command execution (execve syscall)
- Network-related syscalls (socket, connect)
- Process management syscalls (ptrace, kill)

Kernel Module Differences
~~~~~~~~~~~~~~~~~~~~~~~~~

Some kernel modules have different names or availability on ARM64:

- Certain hardware-specific modules don't exist on ARM64
- Filesystem and security modules are generally the same

Validation Steps
~~~~~~~~~~~~~~~~

After running remediation on ARM64:

1. **Verify no architecture-specific failures:**

.. code-block:: console

   # Check for arch-related errors in Ansible output
   ansible-playbook site.yml 2>&1 | grep -i "arch\|arm\|aarch"

2. **Run audit and filter ARM64-specific results:**

.. code-block:: console

   ./run_audit.sh -f json -o audit_arm64.json

   # Check for syscall-related failures
   cat audit_arm64.json | jq '.results[] | select(.title | contains("audit"))'

3. **Compare with x86_64 baseline:**

If possible, run the same benchmark on both architectures and compare:

.. code-block:: console

   # Use diff or a reporting tool to compare results
   diff audit_x86_64.json audit_arm64.json

Troubleshooting
---------------

Audit Binary Issues
~~~~~~~~~~~~~~~~~~~

**Error:** ``goss: cannot execute binary file: Exec format error``

**Cause:** Wrong architecture binary (x86_64 binary on ARM64 system)

**Solution:**

.. code-block:: console

   # Verify current binary architecture
   file /usr/local/bin/goss

   # Download correct ARM64 binary
   curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-arm64 \
       -o /usr/local/bin/goss
   chmod +x /usr/local/bin/goss

auditd Rule Failures
~~~~~~~~~~~~~~~~~~~~

**Symptom:** Many auditd-related controls fail on ARM64 but pass on x86_64

**Cause:** Syscall differences between architectures

**Solution:**

1. Accept that some audit controls will have different results on ARM64
2. Document exceptions in your compliance reporting
3. Use architecture-specific audit rule files if available

Reporting ARM64 Issues
----------------------

When reporting ARM64-specific issues:

1. **Include architecture information:**

.. code-block:: console

   uname -a
   cat /etc/os-release
   lscpu | head -20

2. **Specify the benchmark and version**

3. **Include relevant task output with ``-vvv`` verbosity**

4. **Note if the issue is remediation or audit related**

Report issues at: `Ansible Lockdown GitHub <https://github.com/ansible-lockdown>`_

Best Practices
--------------

1. **Test First**
   Always test ARM64 hardening in non-production before deploying.

2. **Document Exceptions**
   Maintain documentation of controls that behave differently on ARM64.

3. **Use Consistent Images**
   Use the same OS version and ARM64 images across your fleet.

4. **Monitor Audit Results**
   Establish ARM64-specific baselines for audit pass/fail counts.

5. **Stay Updated**
   ARM64 support improves with each release; keep roles updated.

