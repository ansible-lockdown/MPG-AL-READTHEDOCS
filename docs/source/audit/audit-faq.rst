Audit - FAQ
===========

Why does goss run manually fail?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

example.

.. code-block:: bash

   goss -g goss.yml -v

Goss is designed to run from the scripts passing discovered variables into Goss for metadata. Without these values being set, Goss will fail. These metadata variables can bee seen towards the end of the goss.yml file. Futhermore, the run_audit script shows how these variables are created and passed to Goss.


Why do i have different results between x86_64 and AMD65/aarch64 audits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two different hardwares provide different system calls within the OS that auditd is able to utilise. This is often the soure of increased failures vs x86_64. As they are not able to run all commands
