![Build Status](https://img.shields.io/github/workflow/status/ansible-lockdown/RHEL8-CIS/CommunityToDevel?label=Devel%20Build%20Status&style=plastic)
![Build Status](https://img.shields.io/github/workflow/status/ansible-lockdown/RHEL8-CIS/DevelToMain?label=Main%20Build%20Status&style=plastic)
![Release](https://img.shields.io/github/v/release/ansible-lockdown/RHEL8-CIS?style=plastic)

# Documentation for Ansible lockdown documentation

This is presented by readthedocs.io

This is split across multiple folders and strutures

- .readthedocs.yaml - doc for configuration used by read the docs
- requirements.txt - pip requirements file to stipulate the verions on the runner this is built with
- Makefile  - Future use maybe use to assist to build own docs

- source/
  - index.rst - main landing page on readthedocs.io
  - benchmarks.rst - maintained file of whats live/archived and whats covered under ansible-lockdown
  - conf.py - this is the build file how things are put together
  - audit.rst - table of contents for the audit section
  - remediate.rst - TOC for the remediate section
  
- source/audit/      # dir for audit content
- source/remediate/  # dir for the remediate content
- source/_static/MPG-logo-mono-blue.svg

To generate the documentation on a RHEL/CentOS 7 system, take the following steps:

1 Install required packages:

```bash
 yum install python3-pip python-sphinx
```

2 Install the requirements:

``` bash
sudo pip3 install -r requirements.txt
```

3 Generate the documentation:

```bash
make singlehtml
```

## Adding a new benchmark

The file(s) that need to be adjusted are

- source/benchmarks_CIS.rst
- source/benchmarks_STIG.rst

This autopopulates into the index and anywhere else it is required
