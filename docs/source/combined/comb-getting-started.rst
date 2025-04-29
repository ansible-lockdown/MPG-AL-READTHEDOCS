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

Lockdown Facts Example:
-----------------------

Variables Used
--------------

- ``benchmark_version``: The version of the CIS/STIG benchmark being applied.
- **CIS** ``cis_level_1 | cis_level_2``: Booleans that indicate if level 1 or 2 hardening is enabled.
- **STIG** ``stig_cat1 | stig_cat2 | stig_cat3``: Indicate whether Category I, II, or III controls were enabled during the hardening process.
- ``ansible_run_tags``: List of tags used during the playbook run to identify scope
- ``run_audit``: Boolean to indicate if an audit was performed.
- ``audit_log_dir``: Path to local audit log directory on the node.
- ``post_audit_results``: Captured summary results from post-audit steps.
- ``fetch_audit_output``: Boolean flag to indicate whether audit logs were centralized.
- ``audit_output_destination``: Destination directory for centralized audit files.

CIS
+++

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
   audit_run_date = {{ '%Y-%m-%d - %H:%M:%S' | ansible.builtin.strftime }}
   audit_file_local_location = {{ audit_log_dir }}

   {% if not audit_only %}
   audit_summary = {{ post_audit_results }}
   {% endif %}

   {% if fetch_audit_output %}
   audit_files_centralized_location = {{ audit_output_destination }}
   {% endif %}
   {% endif %}

3. **Output**

.. code-block:: ini

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

STIG
----

1. **[lockdown_details]**
   - Contains metadata about the STIG benchmark used, run date, and the hardening levels enabled.

.. code-block:: ini

   [lockdown_details]
   # Benchmark release
   Benchmark_release = STIG-{{ benchmark_version }}
   Benchmark_run_date = {{ '%Y-%m-%d - %H:%M:%S' | ansible.builtin.strftime }}

   # If options set (doesn't mean it ran all controls)
   cat_1_hardening_enabled = {{ rhel9stig_cat1 }}
   cat_2_hardening_enabled = {{ rhel9stig_cat2 }}
   cat_3_hardening_enabled = {{ rhel9stig_cat3 }}

   # Tag-based hardening run types (conditional)
   {% if ansible_run_tags | length > 0 %}
   # If tags used to stipulate run level
   {% if 'rhel9stig_cat1' in ansible_run_tags %}
   Cat_1_Server_tag_run = true
   {% endif %}
   {% if 'rhel9stig_cat2' in ansible_run_tags %}
   Cat_2_Server_tag_run = true
   {% endif %}
   {% if 'rhel9stig_cat3' in ansible_run_tags %}
   Cat_3_Server_tag_run = true
   {% endif %}
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

3. **Output**
   - Contains

.. code-block:: ini

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
                        "benchmark_release": "benchmark_v2r3",
                        "benchmark_run_date": "2025-03-31 - 14:59:43",
                        "cat_1_hardening_enabled": "True",
                        "cat_2_hardening_enabled": "True",
                        "cat_3_hardening_enabled": "True",
                     }
                  }
            },
            "discovered_interpreter_python": "/usr/bin/python3"
         },
         "changed": false
      }
