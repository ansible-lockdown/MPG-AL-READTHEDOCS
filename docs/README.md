# Ansible Lockdown Documentation

[![Documentation Status](https://readthedocs.org/projects/ansible-lockdown/badge/?version=latest)](https://ansible-lockdown.readthedocs.io/en/latest/?badge=latest)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Documentation for Ansible Lockdown security benchmark roles, hosted on [Read the Docs](https://ansible-lockdown.readthedocs.io).

## Project Structure

```
├── .github/
│   └── workflows/main.yml    # CI/CD pipeline
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
├── .pre-commit-config.yaml   # Pre-commit hooks
├── .readthedocs.yaml         # RTD build configuration
└── pyproject.toml            # Python project config
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

Build with live reload (auto-refreshes on changes):

```bash
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

The GitHub Actions workflow (`.github/workflows/main.yml`) runs on push/PR to `main` and `devel` branches:

| Job | Description |
|-----|-------------|
| **build** | Builds Sphinx HTML documentation |
| **linkcheck** | Validates external links |
| **lint** | Runs doc8 and rstcheck |

## Adding Content

### New Benchmark

1. Add entry to the appropriate table in `docs/source/CIS/CIS_table.rst` or `docs/source/STIG/STIG_table.rst`
2. Update `docs/source/intro.rst` if needed
3. Run `pre-commit run --all-files` to validate changes

### New Documentation Page

1. Create `.rst` file in the appropriate directory
2. Add to relevant `toctree` directive in parent document
3. Follow existing formatting conventions

## Dependencies

Dependencies are managed in `requirements/requirements.txt` with pinned versions for reproducible builds. Dependabot automatically creates PRs for updates weekly.

## License

MIT License - see [LICENSE](../LICENSE) for details.
