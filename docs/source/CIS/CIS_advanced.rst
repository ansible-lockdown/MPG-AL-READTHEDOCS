
CIS Specific Information
------------------------

Advanced Options
~~~~~~~~~~~~~~~~

.. note::
   These are advanced options and require a greater understanding of all aspects of implementation.

   - {{ CIS_Role_Name }}_allow_auditd_uid_user_exclusions

auditd logs can fill up very quickly with the default CIS options to log every privileged command.
This is common for scanners, automation, or any job that runs against a system with privileged access, for example through sudo.

There is the ability to change this for specific users to exclude anything in user space.
This will still capture login/logout and sshd process but anything else will be excluded for that user.
This can be enabled with the following (this needs to be set in an alternate variable location):

.. code-block:: yaml

   rhel10cis_allow_auditd_uid_user_exclusions: true


Then add the UIDs of the applicable users to the exclusion list (the role default is ``1999``).
For example (RHEL10-CIS):

.. code-block:: yaml

   rhel10cis_auditd_uid_exclude:
     - 1001
     - 1002
