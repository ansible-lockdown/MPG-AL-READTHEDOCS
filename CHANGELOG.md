# Changelog

All notable changes to the Ansible Lockdown ReadTheDocs documentation will be documented in this file.

## 2026_AUGUST_UPDATES

### Changed
- Corrected the CIS and STIG benchmark tables against the live organization: RHEL10-STIG now
  carries a live release badge instead of Subscribers Only, and SUSE16-CIS and Windows-2025-STIG
  link to their now-public repositories. Both briefly carried an In Development badge and ended the
  cycle marked Subscribers Only.
- Moved Windows-10 and Windows-2016 from the active CIS and STIG availability tables into the
  retired tables, keeping their release badges and setting Maintained to False.
- Brought the Archived Benchmarks list in known_issues into line with those retired tables. It was
  six entries behind: UBUNTU18-STIG, UBUNTU20-STIG, Windows-2016-STIG and Windows-10-STIG were
  missing from the STIG list, and Windows-2016-CIS and Windows-10-CIS from the CIS list. Both lists
  now match their tables exactly, in the same order.
- SUSE16-CIS now carries a live release badge. It published CIS v1.0.0 on 23 September 2026, so the
  Subscribers Only placeholder no longer described it.
- Windows-2025-STIG now carries a live release badge. It published release 1.2.0, based on STIG V1R2,
  on 30 October 2026, so the Subscribers Only placeholder no longer described it.
- Reworded the Windows Server 2025 status in known_issues. It still read Under development, but
  Windows-2025-CIS and Windows-2025-STIG are both publicly released.
- Corrected the Audit column for Windows-11-CIS from NA to WIP. Windows-11-CIS-Audit is public and
  carries a full goss suite, so NA wrongly claimed no audit exists. It has no release, so WIP
  matches how Windows-2022-CIS and Windows-2025-CIS are already described.
- **Windows auditing:** the Audit column for Windows-11-CIS, Windows-2022-CIS and Windows-2025-CIS
  now reads True. Each role runs its public audit repository with Syver on its released branch, and
  the Linux audit repositories marked True publish no releases either, so a release was never the
  test. The
  Audit column for Windows-11-STIG, Windows-2022-STIG and Windows-2025-STIG now reads SCC, with a note
  under the table: those roles scan the host with DISA's SCAP Compliance Checker before and after
  remediation. Getting Started with Audit gains a section on each flow, and the Windows audit known
  issue is scoped to the CIS audit script.
- **Audit column normalized:** UBUNTU18-STIG, UBUNTU20-STIG and Windows-10-CIS now read False, as no
  audit repository exists for them. RHEL6-STIG and Postgres-9-STIG show their release badges, and the
  Windows firewall row is labeled WinFWADV-STIG to match its repository.
- **Site configuration:** `conf.py` is rebuilt for this site. The copied role template titled the
  epub and htmlzip downloads RHEL9-CIS and loaded a leftover extension; both are gone, with
  `.variables.rst`. The build now passes `sphinx-build -W` with no warnings.
- **Navigation:** the Audit FAQ, Remediate FAQ and Known Issues pages are linked under Support. They
  were built but reachable from no menu.
- **Audit binaries:** the audit pages, ARM64 guide, intro and links describe Syver, a fork of Goss,
  and krameff/goss, its earlier name that some roles still pin, through `audit_bin_url` and
  `audit_bin_version`. The upstream v0.4.9 download
  links, two of which returned 404, are removed, and the script excerpts and Windows parameters match
  the current `run_audit.sh` and `run_audit.ps1`.
- **Variable names:** examples across the remediate, audit, container and known issues pages use
  names the roles define (for example `system_is_container`), and the container guide describes the
  detection rule the roles use.
- **Compliance facts, Molecule and release schedule:** the compliance facts section is rewritten from
  the current role templates with valid JSON samples, the Molecule guide is corrected on scenarios,
  drivers, prerequisites and destroy guidance, and the release schedule example is marked
  illustrative.
- **WinRM:** the Remediate FAQ no longer advises enabling Basic authentication or unencrypted
  traffic, which the Windows roles disable; it recommends HTTPS or NTLM/Kerberos.
- **Known issues:** RHEL 10 (Unofficial) is removed, the RHEL8 cloud-init workaround uses the current
  control, and the Windows Server 2025, Amazon Linux 2023 and Ubuntu 24.04 statuses are updated.
- **Contributing and repository docs:** the contributing page describes the approved contributor
  process, signed and signed-off commits, and the devel target. `docs/README.md` and the Makefile
  describe the repository as it is, four unused images are removed, and redirected links point to
  their current addresses.
- UBUNTU26 CIS and STIG remain Coming Soon: the Ubuntu 26.04 benchmarks are not published yet.
  Their rows link to the public UBUNTU26-CIS and UBUNTU26-STIG repositories, which hold no role
  content yet.
- Removed hyperlinks to AAP2-STIG and NGINX-CIS, which are private and returned 404 for public
  readers. Their Subscribers Only and WIP status cells are unchanged.
- Renamed Tyto Athene to Quantum Sky in documentation prose (conf.py copyright, intro and
  support pages). URLs, domains and asset file names are unchanged.
- `LICENSE`: completed the rename the entry above scoped to documentation prose only. The copyright
  line still read `Mindpoint Group - A Tyto Athene Company`, which left it as the last live
  reference to the retired parent company on this repository. It also carried a lowercase `p` in
  `Mindpoint`. Now reads `MindPoint Group - A Quantum Sky Company / Ansible Lockdown`, byte-identical
  to the string carried by the role repositories.
- Pointed the company website links at quantumsky.com, following the prose rename above. The old
  deep paths do not exist on the new site, so the `QuantumSky` link target in intro now goes to the
  site root and the Official Website link in support goes to `/contact`. The LinkedIn and Facebook
  links are unchanged: no Quantum Sky equivalent could be confirmed, and the existing accounts are
  still live.

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
