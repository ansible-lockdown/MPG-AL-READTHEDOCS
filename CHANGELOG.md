# Changelog

All notable changes to the Ansible Lockdown ReadTheDocs documentation will be documented in this file.

## 2026_AUGUST_UPDATES

### Changed
- Corrected the CIS and STIG benchmark tables against the live organisation: RHEL10-STIG now
  carries a live release badge instead of Subscribers Only, and SUSE16-CIS and Windows-2025-STIG
  link to their now-public repositories with an In Development badge until their first release.
- Moved Windows-10 and Windows-2016 from the active CIS and STIG availability tables into the
  retired tables, keeping their release badges and setting Maintained to False.
- UBUNTU26 CIS and STIG remain Coming Soon: the Ubuntu 26.04 benchmarks are not published yet,
  so their rows no longer link to placeholder repositories.
- Removed hyperlinks to AAP2-STIG and NGINX-CIS, which are private and returned 404 for public
  readers. Their Subscribers Only and WIP status cells are unchanged.
- Renamed Tyto Athene to Quantum Sky in documentation prose (conf.py copyright, intro and
  support pages). URLs, domains and asset file names are unchanged.
- `LICENSE`: completed the rename the entry above scoped to documentation prose only. The copyright
  line still read `Mindpoint Group - A Tyto Athene Company`, which left it as the last live
  reference to the retired parent company on this repository. It also carried a lowercase `p` in
  `Mindpoint`. Now reads `MindPoint Group - A Quantum Sky Company / Ansible Lockdown`, byte-identical
  to the string carried by the role repositories.

## 2026_APRIL_UPDATE
### Changed
- Updated CIS_Table for RHEL10CIS via removing "Unofficial"

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
- Fixed .gitignore to exclude docs/build/ directory
