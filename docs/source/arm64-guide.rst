ARM64/aarch64 Architecture Guide
================================

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

2. **Audit Binary:**

When the audit is run by the remediation role (``setup_audit`` / ``run_audit``), the role detects
``aarch64`` and downloads and checksum-verifies the ARM64 binary automatically. A manual download is only
needed for a standalone audit.

The roles use `Syver <https://github.com/krameff/syver/releases>`_ (asset ``syver-linux-arm64``), a fork of Goss, or on some roles its earlier release
under the name `krameff/goss <https://github.com/krameff/goss/releases>`_ (asset ``goss-linux-arm64``). The role's ``audit_bin_url`` and ``audit_bin_version`` defaults show which
one and which release it pins, with the ARM64 checksum.

.. code-block:: console

   # Example: install the release your role pins (replace <release>)
   curl -L https://github.com/krameff/syver/releases/download/<release>/syver-linux-arm64 \
       -o /usr/local/bin/syver
   chmod +x /usr/local/bin/syver

   # Verify installation
   syver --version

3. **Configure Audit Script:**

Set ``AUDIT_BIN`` if the binary is not at the script's default path.

Running Remediation
~~~~~~~~~~~~~~~~~~~

Remediation works the same on ARM64 as x86_64:

.. code-block:: console

   ansible-playbook -i inventory site.yml

No special configuration is needed for most controls.

Running Audit
~~~~~~~~~~~~~

.. code-block:: console

   # Run audit with the binary at a non-default path
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

Legacy syscalls such as ``open``, ``creat``, ``unlink``, ``rename``, ``chmod`` and ``chown`` do not exist
on aarch64; only their ``*at`` variants (for example ``openat`` and ``unlinkat``) do. Benchmark auditd rules
that name the legacy syscalls are therefore affected.

Several roles (for example RHEL10-CIS, RHEL9-CIS, RHEL10-STIG, UBUNTU24-CIS and AMAZON2023-CIS) drop
syscalls the target does not support from the generated rules, using ``ausyscall --dump``. Audit checks that
expect the x86_64 rule text may still report differences.

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

**Error:** ``cannot execute binary file: Exec format error``

**Cause:** Wrong architecture binary (x86_64 binary on ARM64 system)

**Solution:**

.. code-block:: console

   # Verify current binary architecture
   file /usr/local/bin/goss

   # Then download the ARM64 asset of the release your role pins (see Prerequisites above)

auditd Rule Failures
~~~~~~~~~~~~~~~~~~~~

**Symptom:** Many auditd-related controls fail on ARM64 but pass on x86_64

**Cause:** Syscall differences between architectures

**Solution:**

1. Accept that some audit controls will have different results on ARM64
2. Document exceptions in your compliance reporting
3. Check that you are on a role release that filters unsupported syscalls (see Affected Controls above)

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
