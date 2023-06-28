
CIS Specific Information
------------------------

Advanced Options
~~~~~~~~~~~~~~~~

.. note::
   These are advanced options and required a greater understanding of all aspects of implementation.

- auditd_exclusion:

auditd logs can fill up very quickly with the default CIS options to log every privileged commands.
Whether scanners/automation or and job that needs to run against a system with privilege access. e.g.sudo

There is the ability to change this for specific users to exclude anything in user space.
This will still capture login/logout and sshd process but anything else will be excluded for that user.
This can be enabled with the following (this needs to be set in an alternate variable location):

.. code-block:: console

   allow_auditd_uid_user_exclusions: true


Then a list of applicable users can be added to the exclusions.
e.g.


.. code-block:: console

   rhel8cis_auditd_uid_exclude:
   - ansible
   - vagrant

