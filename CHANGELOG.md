# Changelog

All notable changes to the Ansible Lockdown ReadTheDocs documentation will be documented in this file.

## 2026-Q1

### Added
- Added Container and Docker Guide documentation (container-guide.rst)
- Added ARM64/aarch64 Architecture Guide documentation (arm64-guide.rst)
- Added ARM64 Goss binary download links to getting-started-audit.rst
- Added comprehensive CI/CD pipeline with Sphinx build validation, link checking, and RST linting (.github/workflows/main.yml)
- Added pre-commit hooks for code quality (trailing whitespace, YAML validation, RST linting)
- Added .pre-commit-config.yaml with doc8, rstcheck, and yamllint hooks
- Added .doc8.ini configuration for RST linting
- Added dependabot.yml for automated dependency updates (pip and GitHub Actions)
- Added pyproject.toml for modern Python project configuration
- Added requirements-dev.txt for development dependencies
- Added build validation jobs to .readthedocs.yaml (RST linting, link checking)

### Changed
- Pinned dependency versions in requirements.txt for reproducible builds
- Updated GitHub Actions to latest versions (checkout@v4, setup-python@v5, upload-artifact@v4)
- Improved conf.py sys.path configuration to properly load custom extensions
- Modernized docs/README.md with updated project structure, development setup, and CI/CD documentation
- Expanded Remediate FAQ with comprehensive troubleshooting scenarios
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
- Fixed invalid 'raw' lexer in code blocks (audit_development.rst) - changed to 'text'
- Fixed duplicate link target names "Binary"/"Checksum" in getting-started-audit.rst
- Fixed RST list formatting issues in comb-getting-started.rst
- Fixed bash code blocks containing JSON output - changed to 'console'
- Fixed title underline length in intro.rst
- Fixed invalid JSON placeholder in audit-faq.rst
- Fixed bash code block with error message in rem-faq.rst - changed to 'text'
- Fixed trailing whitespace and end-of-file issues across multiple files
