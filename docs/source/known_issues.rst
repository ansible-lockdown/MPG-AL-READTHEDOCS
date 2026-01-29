Known Issues
============

This page documents known issues, bugs, and limitations in the Ansible Lockdown roles.
For troubleshooting common problems, see the :doc:`Audit FAQ </audit/audit-faq>` and
:doc:`Remediate FAQ </remediate/rem-faq>`.

.. contents::
   :local:
   :backlinks: none

Audit Known Issues
------------------

ARM64/aarch64 auditd Syscall Differences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All Linux benchmarks on ARM64 architecture

**Issue:** ARM64 systems use different system call numbers than x86_64. Many auditd-related
controls will fail or produce different results on ARM64 systems.

**Impact:** Audit results will show failures for syscall-based auditd rules.

**Workaround:** This is expected behavior. See :doc:`ARM64 Guide </arm64-guide>` for details
on which controls are affected and how to interpret results.

Goss Timeout on Large Filesystems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All benchmarks with filesystem scanning controls

**Issue:** Controls that scan entire filesystems (e.g., world-writable files, SUID binaries)
can timeout on systems with large numbers of files.

**Impact:** Audit may fail or produce incomplete results.

**Workaround:**

.. code-block:: yaml

   # Increase timeout
   audit_cmd_timeout: 120000

   # Or disable heavy tests
   audit_run_heavy_tests: false

Container Environment Audit Limitations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All benchmarks when ``is_container: true``

**Issue:** Many audit controls assume traditional OS components that don't exist in containers
(systemd, bootloader, kernel modules, auditd).

**Impact:** High number of skipped or failed controls in container audits.

**Workaround:** This is expected. Focus on applicable controls only. See
:doc:`Container Guide </container-guide>`.

Windows Audit Requires Administrator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All Windows benchmarks

**Issue:** Windows audit scripts require Administrator privileges to query security policies,
registry settings, and group policies.

**Impact:** Audit will fail or produce incomplete results without elevation.

**Workaround:** Always run ``run_audit.ps1`` from an elevated PowerShell prompt.

Remediate Known Issues
----------------------

Cloud-init Fails After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:**

- RHEL8-CIS - Control 1.1.3.3
- RHEL8-STIG - RHEL-08-040134

**Issue:** Cloud-init may fail after applying certain filesystem mount options.

**Bug Reference:** `Bug 1839899 <https://bugs.launchpad.net/cloud-init/+bug/1839899>`_

**Workaround:** Disable the affected control if cloud-init is required:

.. code-block:: yaml

   rhel8cis_rule_1_1_3_3: false

SELinux Modules Broken on RHEL 8.6 with EPEL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:**

- RHEL8-CIS
- RHEL8-STIG

**Issue:** All SELinux related Ansible modules are broken on RHEL 8.6 when EPEL packages are active.

**Bug Reference:** `Bug 2093589 <https://bugzilla.redhat.com/show_bug.cgi?id=2093589>`_

**Affected Versions:**

- RHEL 8.6
- Ansible 5.4
- Python 3.8

**Workaround:** Use RHEL-provided Ansible packages instead of EPEL, or upgrade to newer RHEL/Ansible versions.

Python 3.8 Library Issues on RHEL 8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** RHEL 8 systems using Python 3.8

**Issue:** Multiple missing Python 3.8 libraries to support normal Ansible playbook tasks.

**Bug Reference:** `Bug 2093105 <https://bugzilla.redhat.com/show_bug.cgi?id=2093105>`_

**Affected Versions:**

- ansible-core-2.12.2-3.1.el8.x86_64
- ansible-5.4.0-2.el8.noarch
- python38-3.8.12

**Workaround:** Install missing dependencies or use Python 3.9+.

FIPS Mode Breaks Certain Controls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All benchmarks on FIPS-enabled systems

**Issue:** Some cryptographic operations used in controls may fail when FIPS mode is enabled.

**Impact:** Tasks involving non-FIPS-compliant algorithms may fail.

**Workaround:** Review and disable controls that conflict with FIPS requirements.

Grub Password Lockout
^^^^^^^^^^^^^^^^^^^^^

**Affected:** All CIS/STIG benchmarks with bootloader controls

**Issue:** If GRUB password is set but not documented, users may be locked out of system recovery.

**Impact:** Cannot access GRUB menu or boot into rescue mode.

**Prevention:**

.. code-block:: yaml

   # Document your GRUB password before enabling
   rhel9cis_grub_user: root
   rhel9cis_grub_password_hash: "grub.pbkdf2.sha512.10000.YOUR_HASH"

**Recovery:** Boot from rescue media and edit GRUB configuration.

SSH Lockout After Hardening
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Affected:** All benchmarks with SSH controls

**Issue:** SSH configuration changes may prevent login if not properly configured.

**Common Causes:**

- ``AllowUsers``/``AllowGroups`` not including administrative users
- Password authentication disabled without key-based auth configured
- Root login disabled without alternative admin access

**Prevention:**

.. code-block:: yaml

   # Ensure your users are allowed
   rhel9cis_sshd_allow_users: "admin ansible"
   rhel9cis_sshd_allow_groups: "wheel ssh-users"

PAM Lockout Issues
^^^^^^^^^^^^^^^^^^

**Affected:** All benchmarks with PAM controls

**Issue:** Failed login attempt tracking may lock out legitimate users.

**Impact:** Users locked out after failed password attempts.

**Recovery:**

.. code-block:: console

   # Check lockout status
   faillock --user <username>

   # Reset lockout
   faillock --user <username> --reset

Platform-Specific Issues
------------------------

Amazon Linux 2023
^^^^^^^^^^^^^^^^^

**Issue:** Some controls may behave differently due to AL2023's unique package management and systemd configuration.

**Status:** Active development to address differences.

Ubuntu 24.04
^^^^^^^^^^^^

**Issue:** Newer systemd and security features may require control adjustments.

**Status:** Controls updated for Ubuntu 24.04 compatibility.

Windows Server 2025
^^^^^^^^^^^^^^^^^^^

**Issue:** New Windows Server version may have policy changes affecting certain controls.

**Status:** Under development; some controls may need adjustment.

RHEL 10 (Unofficial)
^^^^^^^^^^^^^^^^^^^^

**Issue:** RHEL 10 CIS benchmark is unofficial as CIS has not released an official benchmark.

**Impact:** Controls based on RHEL 9 patterns; may not match future official benchmark.

**Status:** Will be updated when official CIS RHEL 10 benchmark is released.

Deprecation Notices
-------------------

Archived Benchmarks
^^^^^^^^^^^^^^^^^^^

The following benchmarks are archived and no longer actively maintained:

**CIS:**

- RHEL7-CIS
- UBUNTU18-CIS
- UBUNTU20-CIS

**STIG:**

- RHEL5-STIG
- RHEL6-STIG
- RHEL7-STIG
- Windows-2008R2-Member-Server-STIG
- Windows-2012-Member-Server-STIG
- Windows-2012-Domain-Controller-STIG
- Postgres-9-STIG

These remain available but will not receive updates for new benchmark versions or bug fixes.

Reporting New Issues
--------------------

To report a new issue:

1. Check existing issues on GitHub
2. Provide:

   - Benchmark name and version
   - Operating system and version
   - Ansible version
   - Full error message or unexpected behavior
   - Steps to reproduce

3. Submit at: `Ansible Lockdown GitHub <https://github.com/ansible-lockdown>`_

For commercial support: `Lockdown Enterprise <https://lockdownenterprise.com>`_
