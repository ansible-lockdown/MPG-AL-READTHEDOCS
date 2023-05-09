Modifying for Local Use
==============================

Variables and the Role
------------------------

The only location that should be modified is the ``defaults/main.yml`` file. This file only contains the variables that are in bounds for modification in our roles.
Our roles are written in a manor where the intent is everything that could be customized becomes a variable that will be located in ``defaults/main.yml``. The reason
for this is variable precedence. Variables in this location are very low in the hierarchy of variables,
`here is the official list of variable precedence. <https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence>`

How to Edit Variables
---------------------

With using the ``defaults/main.yml`` it gives users much more control on where they these variables. This translates to users changing the variables directly in the
``defaults/main.yml`` file, via ``--extra-vars`` when run from the command line, assigned to hosts/groups in inventory, extra vars in Tower/AAP2 Templates or Projects, and more.

Directly (``defaults/main.yml``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the most basic way to make the change. The file has all of the available variables along with comments on what task the variable is for, a description on what the variable is, and
the formatting for the value in the variable.

Extra-Vars
~~~~~~~~~~

This is where the power of using variables via ``defaults/main.yml`` come into play. Anywhere you can use or set an extra var is place you can set these variables.

CLI In-Line setting (Only run STIG CAT1)
.. code-block:: console

  ansible-playbook -i host_file -e '{ "rhel8stig_cat2_patch":false,"rhel8stig_cat3_patch":false }' ./RHEL8-STIG/site.yml

