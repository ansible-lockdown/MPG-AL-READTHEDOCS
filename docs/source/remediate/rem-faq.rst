Remediate - FAQ
===============

Missing "jmespath" Fatal Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   fatal: [ansible]: FAILED! => {"msg": "You need to install \"jmespath\" prior to running json_query filter"}

This can occur during a playbook run on certain operating systems when patching takes place as part of the playbook due to the way python is implemented.

* `You Need to install jmespath <https://serverfault.com/questions/1114638/ansible-you-need-to-install-jmespath-prior-to-running-json-query-filter-bu>`_ : A great article and explanation written by Discord community member baassssiiee

- NOTE This Should no longer be an issue with new releases as dependency has been removed

Missing Sudo Password (Linux OS Based)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many of the CIS Linux OS based roles remove the ability for sudoers to use the NOPASSWD option to enable elevated privileges.

The user (unless root) that is running the playbook on the target should have a password set and the playbook run accordingly to pass the become_password.

All repositories should now run a pre-req check to ensure that the user does have a password set and will fail if this is not setup.
