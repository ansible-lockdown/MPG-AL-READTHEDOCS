# Ansible Lockdown Documentation

[![Documentation Status](https://readthedocs.org/projects/ansible-lockdown/badge/?version=latest)](https://ansible-lockdown.readthedocs.io/en/latest/?badge=latest)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Documentation for Ansible Lockdown security benchmark roles, hosted on [Read the Docs](https://ansible-lockdown.readthedocs.io).

## Project Structure

```
├── .github/
│   └── workflows/main.yml    # CI lint workflow
├── docs/
│   ├── source/
│   │   ├── conf.py           # Sphinx configuration
│   │   ├── index.rst         # Main landing page
│   │   ├── audit/            # Audit documentation
│   │   ├── remediate/        # Remediate documentation
│   │   ├── combined/         # Combined workflow docs
│   │   ├── CIS/              # CIS benchmark tables
│   │   ├── STIG/             # STIG benchmark tables
│   │   └── _static/          # Images and assets
│   └── Makefile
├── requirements/
│   ├── requirements.txt      # Build dependencies
│   └── requirements-dev.txt  # Development dependencies
├── .doc8.ini                 # doc8 configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
├── .readthedocs.yaml         # RTD build configuration
└── CHANGELOG.md
```

## Local Development

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ansible-lockdown/MPG-AL-READTHEDOCS.git
   cd MPG-AL-READTHEDOCS
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements/requirements-dev.txt
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Building Documentation

Build HTML documentation:

```bash
sphinx-build -b html docs/source docs/build/html
```

Build with live reload (auto-refreshes on changes; `sphinx-autobuild` is not in the requirements files, so install it first):

```bash
pip install sphinx-autobuild
sphinx-autobuild docs/source docs/build/html
```

View the built documentation by opening `docs/build/html/index.html` in a browser.

### Running Quality Checks

Run all pre-commit hooks:

```bash
pre-commit run --all-files
```

Run specific checks:

```bash
# RST linting
doc8 docs/source

# RST syntax checking
rstcheck --recursive docs/source

# Link checking
sphinx-build -b linkcheck docs/source docs/build/linkcheck
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/main.yml`) runs on push and pull request to `main` and `devel`. It has one job, **lint**, which runs doc8 and rstcheck. Both steps report problems but do not fail the job, so check the log.

Read the Docs builds the published site from `main`, using `.readthedocs.yaml`. Run the HTML build and link check above locally before opening a pull request.

## Adding Content

### New Benchmark

1. Add entry to the appropriate table in `docs/source/CIS/CIS_table.rst` or `docs/source/STIG/STIG_table.rst`
2. When retiring a benchmark, move its row to the Archived Roles table and add it to the Archived Benchmarks list in `docs/source/known_issues.rst`
3. Update `docs/source/intro.rst` if needed
4. Run `pre-commit run --all-files` to validate changes

### New Documentation Page

1. Create `.rst` file in the appropriate directory
2. Add to relevant `toctree` directive in parent document
3. Follow existing formatting conventions

## Dependencies

Build dependencies are listed in `requirements/requirements.txt` as version ranges. pre-commit.ci opens pull requests to update the pre-commit hook versions.

## License

MIT License - see [LICENSE](../LICENSE) for details.
