#!/usr/bin/env python3
"""Sphinx configuration for the Ansible Lockdown documentation site."""

# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autosectionlabel',
]

# Make sure the target is unique - allows link to targets on different pages
autosectionlabel_prefix_document = True

source_suffix = '.rst'
master_doc = 'index'

project = 'Ansible Lockdown'
author = 'Ansible Lockdown'
copyright = '2026, MindPoint Group - A Quantum Sky Company'
title = 'Ansible Lockdown Documentation'
description = 'CIS and STIG compliance auditing and remediation with Ansible and Goss'
category = 'Security'

# Base name for the builder output files (epub, htmlzip, LaTeX, man, Texinfo)
target_name = 'ansible-lockdown'

language = 'en'
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'prev_next_buttons_location': 'bottom',
    'sticky_navigation': True,
    'collapse_navigation': False,
}

html_title = 'Ansible Lockdown'
html_logo = '_static/LockdownEnterprise-MPG-White_V1.svg'
html_static_path = ['_static']
html_last_updated_fmt = '%Y-%m-%d %H:%M'
html_use_index = False
html_show_copyright = True
htmlhelp_basename = target_name + '-docs'

# If true, publish source files
html_copy_source = False

# -- Options for other builders -------------------------------------------

epub_title = title

latex_documents = [
    (master_doc, target_name + '.tex', title, author, 'manual'),
]

man_pages = [
    (master_doc, target_name, title, [author], 1),
]

texinfo_documents = [
    (master_doc, target_name, title, author, project, description, category),
]
