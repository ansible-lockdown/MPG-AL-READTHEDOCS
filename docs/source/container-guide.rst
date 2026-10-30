Container and Docker Guide
==========================

.. contents::
   :local:
   :backlinks: none

Overview
--------

Running Ansible Lockdown roles in containerized environments requires special considerations.
Containers differ from traditional VMs or bare-metal systems in several important ways that
affect security benchmarking and remediation.

.. warning::

   Security benchmarks (CIS and STIG) are primarily designed for traditional operating systems,
   not containers. Many controls may not apply or could break container functionality.
   Always test thoroughly in non-production environments.

Container Detection
-------------------

The Linux remediation roles include automatic container detection to skip controls that are
incompatible with containerized environments. This is controlled through the ``system_is_container``
variable.

**Automatic Detection**

The roles treat the target as a container when either of these is true:

- The Ansible connection is ``docker`` (some roles also accept ``community.docker.docker``)
- The ``virtualization_type`` fact is ``docker``, ``lxc``, ``openvz``, ``podman`` or ``container``

When detection fires, the role sets ``system_is_container: true`` and loads the container rule set
from ``vars/is_container.yml`` (the file name is set by ``container_vars_file``).

**Manual Override**

``system_is_container`` is defined in each role's ``vars/main.yml``, which outranks playbook and
inventory variables. To force it, pass it as an extra var:

.. code-block:: console

   ansible-playbook site.yml -e system_is_container=true

This only gates the tasks that test ``system_is_container``. To apply the container rule set as well,
also pass the role's file (for example ``-e @vars/is_container.yml``), or connect with the docker
connection so detection runs.

Controls Skipped in Containers
------------------------------

When running in container mode, certain controls are automatically skipped because they:

- Require kernel-level access (not available in containers)
- Depend on systemd services (containers typically use a single process)
- Modify boot configurations (containers don't boot traditionally)
- Require hardware access (containers are abstracted from hardware)

**Common Skipped Categories:**

The exact set differs per role; see the role's ``vars/is_container.yml``. Typical categories are:

- Bootloader configuration and the kernel command line
- Separate partitions and mount options
- Kernel module management
- auditd configuration (requires host kernel support)
- Firewall rules (managed at host level)
- SELinux or AppArmor
- Time synchronization (most roles; handled by the host)

Running Audit in Containers
---------------------------

Audit from Host Against Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also audit a running container from the host using the ``community.docker.docker_container_exec`` module.
The audit content sits at ``{audit_conf_dest}/{benchmark}-Audit``, which defaults to ``/opt/RHEL10-CIS-Audit`` for RHEL10-CIS:

.. code-block:: yaml

   - hosts: localhost
     connection: local
     tasks:
       - name: Run audit against container
         community.docker.docker_container_exec:
           container: my_container
           command: /opt/RHEL10-CIS-Audit/run_audit.sh

Running Remediation in Containers
---------------------------------

Building Hardened Container Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The recommended approach is to build hardened base images rather than remediating running containers.
Run the role against a build container through the docker connection, then commit that container as your image:

.. code-block:: yaml

   # playbook for building hardened images
   - hosts: image_build_container
     connection: community.docker.docker
     roles:
       - role: RHEL10-CIS

Remediating Running Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While not recommended for production, you can remediate running containers for testing:

.. code-block:: yaml

   - hosts: container_hosts
     connection: docker
     vars:
       # Example: skip an individual control
       # (the container rule set already disables bootloader controls such as this one)
       rhel10cis_rule_1_4_1: false
     roles:
       - RHEL10-CIS

.. warning::

   Running privileged containers for auditing requires careful consideration of your
   security requirements. Limit access and use RBAC appropriately.

Known Limitations
-----------------

**Controls That Cannot Work in Containers:**

.. csv-table:: Container Incompatible Controls
   :header: "Category", "Reason", "Alternative"
   :widths: 30, 40, 30

   "Bootloader (GRUB)", "Containers don't have bootloaders", "Apply to host OS"
   "Kernel parameters (sysctl)", "Requires host kernel access (disabled in some roles)", "Apply to host OS"
   "Partition mounts", "Container filesystems are overlays", "Use read-only containers"
   "auditd rules", "Requires host auditd", "Use container runtime logging"
   "Firewall (iptables/nftables)", "Managed at host/orchestrator level", "Use network policies"
   "Time sync (chrony/ntp)", "Containers use host time (disabled in most roles)", "Apply to host OS"

**auditd in Containers:**

The auditd subsystem requires kernel-level access. For container environments:

- Configure auditd on the container host
- Use container runtime audit logging (Docker audit, containerd events)

Best Practices
--------------

1. **Harden the Host First**
   Apply full CIS/STIG benchmarks to container hosts before focusing on containers.

2. **Use Minimal Base Images**
   Start with a minimal image of the distribution the role targets (for example UBI-minimal or Rocky minimal
   for the RHEL roles) to reduce attack surface.

3. **Build Immutable Images**
   Apply hardening at image build time, not runtime. Treat containers as immutable.

4. **Scan Images in CI/CD**
   Integrate audit into your image build pipeline to catch issues before deployment.

Troubleshooting
---------------

**Playbook fails on service tasks in a container**

Containers without systemd cannot start or enable services. Check that container detection ran,
or force container mode as described under Manual Override:

.. code-block:: console

   ansible-playbook site.yml -e system_is_container=true

**Audit shows many failures for kernel controls**

Container audits will fail kernel-related checks by design. Filter results:

.. code-block:: console

   # Show only non-skipped results
   jq '.results[] | select(.skipped != true)' audit_output.json

**Permission denied errors**

Containers may need elevated privileges for certain audits:

.. code-block:: console

   docker run --privileged --pid=host your-audit-image

.. note::

   Running privileged containers should only be done in controlled environments
   for auditing purposes.
