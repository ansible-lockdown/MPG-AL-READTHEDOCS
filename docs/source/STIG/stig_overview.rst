
STIG Overview
-------------

What is STIG?
~~~~~~~~~~~~~

Sometimes refered to as DISA STIG.
DISA STIG refers to an organization (DISA — Defense Information Systems Agency) that provides technical guides (STIG — Security Technical Implementation Guide).


What does this role do?
~~~~~~~~~~~~~~~~~~~~~~~


This role follows the  Security Technical Implementation Guide (STIG) released for the OS/Platform/application.
Each guide is different, some have in excess of 200 controls and apply to various part of an OS but each guide is
updated regularly by (DISA).

.. note::
   DISA is part of the United States Department of Defense.


Control Severities
~~~~~~~~~~~~~~~~~~

Controls are divided into groups based on the following properties:

- **High (CAT I)**
  These controls have a large impact on the security of a
  system. They also have the largest operational impact to a system and
  deployers should test them thoroughly in non-production environments.

- **Medium (CAT II)**
  These controls are the bulk of the items in the STIG and
  they have a moderate level of impact on the security of a system.
  Many controls in this category will have an operational impact on
  a system and should be tested thoroughly before implementation.

- **Low (CAT III)**
  These controls have a smaller impact on overall security, but they
  are generally easier to implement with a much lower operational impact.

.. note::

   All of the default configurations are found within
   - remediation - ``defaults/main.yml``
   - audit
     - standalone ``vars/STIG.yml``
     - combined ``vars/[system_hostname].yml``
