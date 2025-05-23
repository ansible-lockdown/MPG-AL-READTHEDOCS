Audit - FAQ
===========

Why does goss run manually fail?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

example.

.. code-block:: bash

   goss -g goss.yml -v

Goss is designed to run from the scripts passing discovered variables into Goss for metadata. Without these values being set, Goss will fail. These metadata variables can bee seen towards the end of the goss.yml file. Furthermore, the run_audit script shows how these variables are created and passed to Goss.


Why do I have different results between x86_64 and AMD64/aarch64 audits?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two different hardware architectures provide distinct system calls within the OS that auditd can utilize. This is often the source of increased failures compared to x86_64, as they are unable to execute all commands.
