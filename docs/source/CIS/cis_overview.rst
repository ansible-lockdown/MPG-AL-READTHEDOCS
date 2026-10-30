
CIS Overview
------------

What is CIS?
~~~~~~~~~~~~

**Center for Internet Security**

**CIS** is home to the Multi-State Information Sharing and Analysis Center® (MS-ISAC®),
the trusted resource for cyber threat prevention, protection, response, and recovery
for U.S. State, Local, Tribal, and Territorial government entities,
and the Elections Infrastructure Information Sharing and Analysis Center® (EI-ISAC®),
which supports the rapidly changing cybersecurity needs of U.S. elections offices.


What do the CIS roles do?
~~~~~~~~~~~~~~~~~~~~~~~~~


The roles follow the guide (benchmark) that CIS releases for each OS, platform or application.
Each guide is different; some have more than 200 controls that apply to various parts of an
OS, platform or application. CIS updates each guide regularly.

.. note::
   CIS is often used when no suitable STIG has been released.

Control Severities
~~~~~~~~~~~~~~~~~~

Controls are divided into groups based on the following properties:

- **Level 1**
  The majority of controls are at this level.
  These controls are intended to be practical and to have a low impact on a system,
  with a low to medium risk of disruption when implemented.

- **Level 2**
  These controls are intended for environments where security is paramount (defense in depth).
  They carry a higher risk of system disruption when implemented.

.. note::
    Levels are also split by profile, server or workstation. A control can be Level 1 for servers and Level 2 for
    workstations, or the reverse. We tag each task with the full profile, e.g. level1-server or level1-workstation.

.. note::

   All of the default configurations should be adjusted via variable files, not within the tasks themselves.

   - remediation - ``defaults/main.yml``
   - audit

     - standalone ``vars/CIS.yml``
     - combined ``vars/[system_hostname].yml``

   Container environments are detected automatically and skip controls that are incompatible with containers.
   See :doc:`Container Guide </container-guide>` for details.
