ARM64/aarch64 Architecture Guide
=================================

.. contents::
   :local:
   :backlinks: none

Overview
--------

With the growing adoption of ARM64 (aarch64) processors in servers, cloud instances (AWS Graviton,
Azure Ampere, Google Tau T2A), and edge computing, Ansible Lockdown has extended support
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

Supported Benchmarks
--------------------

The following benchmarks have been tested on ARM64 systems:

.. csv-table:: ARM64 Benchmark Support
   :header: "Benchmark", "Remediate", "Audit", "Notes"
   :widths: 25, 15, 15, 45

   "AMAZON2-CIS", "Yes", "Partial", "Graviton instances supported"
   "AMAZON2023-CIS", "Yes", "Partial", "Graviton instances supported"
   "RHEL8-CIS", "Yes", "Partial", "auditd syscall differences"
   "RHEL9-CIS", "Yes", "Partial", "auditd syscall differences"
   "RHEL8-STIG", "Yes", "Partial", "auditd syscall differences"
   "RHEL9-STIG", "Yes", "Partial", "auditd syscall differences"
   "UBUNTU22-CIS", "Yes", "Partial", "auditd syscall differences"
   "UBUNTU24-CIS", "Yes", "Partial", "auditd syscall differences"

.. note::

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

.. csv-table:: auditd Syscall Differences
   :header: "x86_64 Syscall", "ARM64 Equivalent", "Status"
   :widths: 30, 30, 40

   "open", "openat", "Use openat on ARM64"
   "creat", "openat (with flags)", "Different implementation"
   "rename", "renameat/renameat2", "Use renameat variants"
   "rmdir", "unlinkat", "Different syscall"
   "unlink", "unlinkat", "Different syscall"
   "chmod", "fchmodat", "Use fchmodat"
   "chown", "fchownat", "Use fchownat"
   "lchown", "fchownat", "Use fchownat"
   "link", "linkat", "Different syscall"
   "symlink", "symlinkat", "Different syscall"
   "mknod", "mknodat", "Different syscall"
   "mount", "mount", "Same (supported)"
   "umount", "umount2", "Slightly different"

**Workaround - Architecture-Specific Audit Rules:**

For environments requiring accurate auditd monitoring on ARM64, use architecture-aware rules:

.. code-block:: bash

   # Example: File deletion monitoring
   # x86_64 rule
   -a always,exit -F arch=b64 -S unlink,unlinkat,rename,renameat -F auid>=1000 -F auid!=unset -k delete

   # ARM64 equivalent (unlink doesn't exist, only unlinkat)
   -a always,exit -F arch=b64 -S unlinkat,renameat,renameat2 -F auid>=1000 -F auid!=unset -k delete

**Configuration Option:**

Some roles provide an option to use ARM64-compatible audit rules:

.. code-block:: yaml

   # In your playbook or host_vars
   use_arm64_audit_rules: true

.. note::

   Check your specific benchmark role's ``defaults/main.yml`` for available ARM64 options.

Kernel Module Differences
~~~~~~~~~~~~~~~~~~~~~~~~~

Some kernel modules have different names or availability on ARM64:

- Certain hardware-specific modules don't exist on ARM64
- Filesystem and security modules are generally the same

Package Availability
~~~~~~~~~~~~~~~~~~~~

Most packages are available for ARM64 in enterprise Linux distributions. However:

- Some third-party security tools may lack ARM64 builds
- EPEL ARM64 support may lag behind x86_64

Cloud-Specific Considerations
-----------------------------

AWS Graviton
~~~~~~~~~~~~

AWS Graviton processors (Graviton2, Graviton3) are ARM64-based. When running on Graviton:

.. code-block:: yaml

   # Detect Graviton instances
   - name: Check if running on Graviton
     ansible.builtin.set_fact:
       is_graviton: "{{ ansible_processor[1] is search('Graviton') }}"
     when: ansible_system == 'Linux'

**Graviton-Specific Notes:**

- Amazon Linux 2 and 2023 on Graviton are well-tested
- EBS and instance store work identically to x86_64
- Nitro security features are available

Azure Ampere
~~~~~~~~~~~~

Azure Ampere Altra processors:

- Use standard RHEL/Ubuntu ARM64 images
- Azure-specific extensions work on ARM64
- Network and storage controls apply normally

Google Cloud Tau T2A
~~~~~~~~~~~~~~~~~~~~

Google's ARM64 VMs:

- Standard Linux distributions supported
- Container-Optimized OS has ARM64 support
- GKE ARM64 node pools available

Testing ARM64 Deployments
-------------------------

Test Environment Setup
~~~~~~~~~~~~~~~~~~~~~~

For testing ARM64 hardening:

**Option 1: Cloud Instance**

.. code-block:: console

   # AWS Graviton example
   aws ec2 run-instances \
     --instance-type t4g.medium \
     --image-id ami-xxxxxxxxx \  # ARM64 AMI
     --key-name your-key

**Option 2: QEMU Emulation**

For local testing without ARM64 hardware:

.. code-block:: console

   # Install QEMU
   sudo apt-get install qemu-system-aarch64

   # Run ARM64 VM
   qemu-system-aarch64 -machine virt -cpu cortex-a72 \
     -m 2048 -nographic \
     -drive file=arm64-image.qcow2,if=virtio

**Option 3: Docker with Multi-Architecture**

.. code-block:: console

   # Run ARM64 container on x86_64 (requires QEMU binfmt)
   docker run --platform linux/arm64 -it rockylinux:9 /bin/bash

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
4. Consider using alternative monitoring (eBPF-based tools like Falco)

Missing Kernel Modules
~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``modprobe: FATAL: Module xyz not found``

**Cause:** Module doesn't exist or has different name on ARM64

**Solution:**

.. code-block:: console

   # Check available modules
   find /lib/modules/$(uname -r) -name "*.ko*" | grep -i <module_name>

   # Verify module status
   lsmod | grep <module_name>

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

6. **Consider Compensating Controls**
   For auditd limitations, consider:

   - eBPF-based monitoring (Falco, Tetragon)
   - Application-level logging
   - Cloud provider audit logs (CloudTrail, Azure Activity Log)
