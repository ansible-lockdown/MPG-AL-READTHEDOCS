Using Audit and Remediate together
==========================================

Using both Audit and Remediate in a workflow

This is missing the copy remediate settings step

.. image:: ../_static/rem_initiated_audit.png
   :height: 400px
   :width: 1000px
   :align: center
   :alt: Process Workflow Audit and Remediate


Post Hardening Lockdown Reporting via Ansible_Facts
===================================================

The `etc/ansible/compliance_facts.j2` template metadata and conditions related to hardening performed by the **Ansible Lockdown** role.

File Sections
-------------

Example:

1. **[lockdown_details]**
   - Contains metadata about the CIS benchmark used, run date, and the hardening levels enabled.

.. code-block:: ini

    [lockdown_details]
    # Benchmark release
    Benchmark_release = CIS-{{ benchmark_version }}
    Benchmark_run_date = {{ '%Y-%m-%d - %H:%M:%S' | ansible.builtin.strftime }}

    # Hardening levels enabled via variables
    level_1_hardening_enabled = {{ rhel9cis_level_1 }}
    level_2_hardening_enabled = {{ rhel9cis_level_2 }}

    # Tag-based hardening run types (conditional)
    {% if 'level1-server' in ansible_run_tags %}
    Level_1_Server_tag_run = true
    {% endif %}
    {% if 'level2-server' in ansible_run_tags %}
    Level_2_Server_tag_run = true
    {% endif %}
    {% if 'level1-workstation' in ansible_run_tags %}
    Level_1_workstation_tag_run = true
    {% endif %}
    {% if 'level2-workstation' in ansible_run_tags %}
    Level_2_workstation_tag_run = true
    {% endif %}

2. **[lockdown_audit_details]**
   - Captures audit-specific information if auditing is enabled.

.. code-block:: ini

    [lockdown_audit_details]
    {% if run_audit %}
    # Audit run
    audit_file_local_location = {{ audit_log_dir }}

    {% if not audit_only %}
    audit_summary = {{ post_audit_results }}
    {% endif %}

    {% if fetch_audit_output %}
    audit_files_centralized_location = {{ audit_output_destination }}
    {% endif %}
    {% endif %}

Variables Used
--------------

- ``benchmark_version``: The version of the CIS benchmark being applied.
- ``rhel9cis_level_1 / level_2``: Booleans that indicate if level 1 or 2 hardening is enabled.
- ``ansible_run_tags``: List of tags used during the playbook run to identify scope (e.g., server/workstation level 1/2).
- ``run_audit``: Boolean to indicate if an audit was performed.
- ``audit_log_dir``: Path to local audit log directory on the node.
- ``post_audit_results``: Captured summary results from post-audit steps.
- ``fetch_audit_output``: Boolean flag to indicate whether audit logs were centralized.
- ``audit_output_destination``: Destination directory for centralized audit files.

Output Example:

.. code-block:: yaml

      ansible hosts -i ../inv -m setup -a "filter=ansible_local"
      hosts | SUCCESS => {
         "ansible_facts": {
            "ansible_local": {
                  "lockdown_facts": {
                     "Benchmark_Audit_Details": {
                        "audit_file_location_local": "/opt",
                        "audit_summary": "Count: 798, Failed: 24, Skipped: 6, Duration: 38.824s"
                     },
                     "Benchmark_Details": {
                        "benchmark_release": "CIS-v2.0.0",
                        "benchmark_run_date": "2025-03-31 - 14:59:43",
                        "level_1_hardening_enabled": "True",
                        "level_2_hardening_enabled": "True"
                     }
                  }
            },
            "discovered_interpreter_python": "/usr/bin/python3"
         },
         "changed": false
      }
