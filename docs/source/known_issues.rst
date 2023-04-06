Known Issues
------------


Audit
^^^^^



Remediate
^^^^^^^^^

**Cloud init fails** `Bug 1839899 <https://bugs.launchpad.net/cloud-init/+bug/1839899>`_

    Affects

    - RHEL8-CIS -  1.1.3.3
    - RHEL8-STIG - RHEL-08-040134

**All SELinux related modules are currently broken on RHEL8.6 with epel packages active.** `Bug 2093589 <https://bugzilla.redhat.com/show_bug.cgi?id=2093589>`_

    Affects

    Version-Release number of selected component (if applicable):
    REHL8.6
    Ansible 5.4
    Python 3.8

**Multiple missing Python 3.8 libraries to support normal Ansible playbook tasks.** `Bug 2093105 <https://bugzilla.redhat.com/show_bug.cgi?id=2093105>`_

    Affects

    Version-Release number of selected component (if applicable):

    ansible-core-2.12.2-3.1.el8.x86_64
    ansible-5.4.0-2.el8.noarch
    python38-3.8.12