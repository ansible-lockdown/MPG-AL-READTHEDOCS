# Changelog

All notable changes to the Ansible Lockdown ReadTheDocs documentation will be documented in this file.

## 2026-Q1

### Added
- Added Container and Docker Guide documentation (container-guide.rst)
- Added ARM64/aarch64 Architecture Guide documentation (arm64-guide.rst)
- Added ARM64 Goss binary download links to getting-started-audit.rst

### Changed
- Expanded Remediate FAQ with comprehensive troubleshooting scenarios (connection issues, Python dependencies, playbook execution, configuration, service issues, performance, rollback)
- Expanded Audit FAQ with detailed troubleshooting (Goss binary issues, result interpretation, performance, script configuration, Windows-specific, container environments)
- Expanded Known Issues with audit issues, remediate issues, platform-specific issues, and deprecation notices
- Updated copyright year to 2026 in conf.py
- Updated License year to 2026
- Updated CIS table with DEBIAN13-CIS benchmark
- Moved UBUNTU18-CIS and UBUNTU20-CIS to Archived Roles section
- Updated Archive tables statuses
- Updated STIG and CIS table statuses to Subscribers Only for DEB13CIS & AMZ23STIG
- Clarified container configuration note in CIS overview
- Expanded ARM64 FAQ entry with detailed explanation of audit differences
- Updated intro.rst ARM64 section with cloud provider examples and guide reference

### Fixed
- Fixed typo "Priority big fixes" to "Priority bug fixes" in links.rst
- Fixed typo "REHL8.6" to "RHEL8.6" in known_issues.rst
- Fixed grammar "These controls have are considered" to "These controls are considered" in cis_overview.rst
- Fixed typo "configures" to "configured" in Security_remediation_and_auditing.md
