Audit - FAQ
===========

Why does goss run manually fail?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

example.

.. code-block:: bash

   goss -g goss.yml -v

Goss is designed to run from the scripts passing discovered variables into Goss for metadata. Without these values being set, Goss will fail. These metadata variables can bee seen towards the end of the goss.yml file. Furthermore, the run_audit script shows how these variables are created and passed to Goss.


Why do I have different results between x86_64 and AMD64/aarch64 audits?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two different hardware architectures provide distinct system calls within the OS that auditd can utilize. This is often the source of increased failures compared to x86_64, as they are unable to execute all commands.


My System is impacted when running the audit how can i restrict its affect?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On both windows and linux you have the ability to limit the number of processes that run at the same time.

This is set the variable as art of the playbook

.. code-block:: bash

   audit_max_concurrent

or if running manually using the run_audit script

.. code-block:: bash

   -m #

It is also possible on linux to change the priority of a process by using nice

- `set process priorities <https://www.howtogeek.com/411979/how-to-set-process-priorities-with-the-nice-and-renice-commands-in-linux/>`_
