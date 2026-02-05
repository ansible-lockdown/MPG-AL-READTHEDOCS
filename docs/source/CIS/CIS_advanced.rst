
CIS Specific Information
------------------------

Advanced Options
~~~~~~~~~~~~~~~~

.. note::
   These are advanced options and require a greater understanding of all aspects of implementation.

   - {{ CIS_Role_Name }}_allow_auditd_uid_user_exclusions

auditd logs can fill up very quickly with the default CIS options to log every privileged command.
Whether scanners/automation or any job that needs to run against a system with privilege access. e.g.sudo

There is the ability to change this for specific users to exclude anything in user space.
This will still capture login/logout and sshd process but anything else will be excluded for that user.
This can be enabled with the following (this needs to be set in an alternate variable location):

.. code-block:: console

   rhel10cis_allow_auditd_uid_user_exclusions: true


Then a list of applicable users can be added to the exclusions.
e.g.


.. code-block:: console

   rhel10cis_auditd_uid_exclude:
   - ansible
   - vagrant
