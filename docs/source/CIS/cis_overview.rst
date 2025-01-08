
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


The roles follow the CIS provided guide (benchmark) released for the OS/platform/application.
Each guide is different, some have in excess of 200 controls and apply to various parts of an
OS/platform/application. Each guide is updated regularly by CIS.

.. note::
   CIS is often used if there is absence for an appropriate released STIG version.

Control Severities
~~~~~~~~~~~~~~~~~~

Controls are divided into groups based on the following properties:

- **Level 1**
  The majority of control are based at this level.
  These controls have are considered to have a low impact to a system.
  By implementing these controls is considered low to medium risk of disruption.

- **Level 2**
  These controls are considered high risk with a chance of system disruption if implemented.

.. note::
    Along with severities it also shows the severity for servers vs workstations. You can have a control that is more
    severe for servers than workstations or vice-versa. We tag each task with the full level, level1-server/level1-workstation

.. note::

   All of the default configurations are found within is_container.yml and this is where they should be adjusted. Do not adjust within the tasks themselves

   - remediation - ``defaults/main.yml``
   - audit

     - standalone ``vars/CIS.yml``
     - combined ``vars/[system_hostname].yml``
