Audit and remediate combined FAQs
---------------------------------

Does this role work only with the specified OS?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Linux


The |benchmark_name| guidance is designed to ONLY be applicable to the listed OS
systems and if you are using this role in a regulated organization you should be aware
that applying these settings to distributions other than listed is unsupported
and may run afoul of your organization or regulatory bodies guidelines during a compliance
audit. It is on YOU to understand your organizations requirements and the laws and regulations
you must adhere to before applying this role.

- Windows


For Windows based benchmarks these are specific to the generation e.g. 2019.
While many controls are the same across these generational releases
The packages that are available to the OS e.g. .NET or powershell versions
may not always function the same way and the roles are adjusted where required.


Which systems are covered?
^^^^^^^^^^^^^^^^^^^^^^^^^^

This role and the |benchmark_name| guidance it implements are fully applicable to servers
(physical or virtual) and containers running the following distributions:

* |benchmark_os|



The role is tested against each distribution to ensure that tasks run properly.
it is idempotent, and  an Audit is used to run a compliance scan after the role
is applied to test compliance with the STIG standard.

Which systems are not covered?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This role will run properly against a container (docker or other), however
this is not recommended and is only really useful during the development and
testing of this role (ie most CI systems provide containers and not full VMs),
so this role must be able to run on and test against containers.

Again for those in the back...applying this role against a container
in order to secure it is generally a *BAD* idea. You should be applying this
role to your container hosts and then using other hardening guidance that is
specific to the container technology you are using (docker, lxc, lxd, etc)
