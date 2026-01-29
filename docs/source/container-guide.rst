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

The Ansible Lockdown roles include automatic container detection to skip controls that are
incompatible with containerized environments. This is controlled through the ``is_container``
variable.

**Automatic Detection**

The roles attempt to detect if they are running inside a container by checking for:

- Presence of ``/.dockerenv`` file
- Container-related entries in ``/proc/1/cgroup``
- Systemd not running as PID 1

**Manual Override**

You can manually specify container mode by setting the variable:

.. code-block:: yaml

   # In your playbook or extra vars
   is_container: true

Controls Skipped in Containers
------------------------------

When running in container mode, certain controls are automatically skipped because they:

- Require kernel-level access (not available in containers)
- Depend on systemd services (containers typically use a single process)
- Modify boot configurations (containers don't boot traditionally)
- Require hardware access (containers are abstracted from hardware)

**Common Skipped Categories:**

- Bootloader configurations (GRUB, kernel parameters)
- Partition and mount configurations
- Kernel module management
- auditd configuration (requires host kernel support)
- Network firewall rules (managed at host level)
- Time synchronization (handled by host)

Running Audit in Containers
---------------------------

Standalone Container Audit
~~~~~~~~~~~~~~~~~~~~~~~~~~

To run an audit inside a container:

1. **Build an audit container image:**

.. code-block:: dockerfile

   FROM your-base-image:tag

   # Install goss binary
   RUN curl -L https://github.com/aelsabbahy/goss/releases/download/v0.4.9/goss-linux-amd64 \
       -o /usr/local/bin/goss && \
       chmod +x /usr/local/bin/goss

   # Copy audit content
   COPY audit-content/ /opt/audit/

   # Set working directory
   WORKDIR /opt/audit

2. **Run the audit:**

.. code-block:: console

   docker run --rm your-audit-image /opt/audit/run_audit.sh

.. note::

   Container audits will show many "skipped" results for controls that don't apply
   to containerized environments. This is expected behavior.

Audit from Host Against Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also audit a running container from the host using Ansible's ``docker`` connection:

.. code-block:: yaml

   - hosts: localhost
     connection: local
     tasks:
       - name: Run audit against container
         community.docker.docker_container_exec:
           container: my_container
           command: /opt/audit/run_audit.sh

Running Remediation in Containers
---------------------------------

Building Hardened Container Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The recommended approach is to build hardened base images rather than remediating running containers:

.. code-block:: yaml

   # playbook for building hardened images
   - hosts: localhost
     connection: local
     vars:
       is_container: true
     roles:
       - role: RHEL9-CIS
         when: ansible_os_family == 'RedHat'

**Multi-stage Dockerfile Example:**

.. code-block:: dockerfile

   # Stage 1: Apply hardening
   FROM rhel9:latest AS hardening

   # Install Ansible
   RUN dnf install -y ansible-core python3-pip && \
       pip3 install ansible

   # Copy and run hardening playbook
   COPY hardening-playbook.yml /tmp/
   COPY RHEL9-CIS/ /tmp/RHEL9-CIS/
   RUN ansible-playbook -c local -i localhost, /tmp/hardening-playbook.yml

   # Stage 2: Clean image
   FROM hardening AS final

   # Remove Ansible and build dependencies
   RUN dnf remove -y ansible-core python3-pip && \
       dnf clean all && \
       rm -rf /tmp/*

   # Your application setup
   COPY app/ /app/

Remediating Running Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While not recommended for production, you can remediate running containers for testing:

.. code-block:: yaml

   - hosts: container_hosts
     connection: docker
     vars:
       is_container: true
       # Disable controls that require reboot
       rhel9cis_rule_1_4_1: false  # Example: skip bootloader password
     roles:
       - RHEL9-CIS

Kubernetes and OpenShift
------------------------

For Kubernetes environments, consider these approaches:

**Pod Security Standards**

Instead of applying CIS/STIG controls directly, use Kubernetes-native security:

- Pod Security Admission (PSA)
- Network Policies
- Security Contexts
- OPA/Gatekeeper policies

**DaemonSet for Auditing**

Deploy audit as a DaemonSet to scan nodes:

.. code-block:: yaml

   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     name: security-audit
   spec:
     selector:
       matchLabels:
         app: security-audit
     template:
       metadata:
         labels:
           app: security-audit
       spec:
         hostPID: true
         hostNetwork: true
         containers:
         - name: audit
           image: your-audit-image:tag
           securityContext:
             privileged: true
           volumeMounts:
           - name: host-root
             mountPath: /host
             readOnly: true
         volumes:
         - name: host-root
           hostPath:
             path: /

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
   "Kernel parameters (sysctl)", "Requires host kernel access", "Apply to host OS"
   "Partition mounts", "Container filesystems are overlays", "Use read-only containers"
   "auditd rules", "Requires host auditd", "Use container runtime logging"
   "PAM configuration", "Often not applicable", "Use container user namespaces"
   "Firewall (iptables/nftables)", "Managed at host/orchestrator level", "Use network policies"
   "Time sync (chrony/ntp)", "Containers use host time", "Apply to host OS"

**auditd in Containers:**

The auditd subsystem requires kernel-level access. For container environments:

- Configure auditd on the container host
- Use container runtime audit logging (Docker audit, containerd events)
- Consider Falco for container-native runtime security

Best Practices
--------------

1. **Harden the Host First**
   Apply full CIS/STIG benchmarks to container hosts before focusing on containers.

2. **Use Minimal Base Images**
   Start with minimal images (alpine, distroless, UBI-minimal) to reduce attack surface.

3. **Build Immutable Images**
   Apply hardening at image build time, not runtime. Treat containers as immutable.

4. **Scan Images in CI/CD**
   Integrate audit into your image build pipeline to catch issues before deployment.

5. **Layer Security Controls**
   Combine benchmark hardening with:

   - Image vulnerability scanning
   - Runtime security monitoring
   - Network policies
   - Secrets management

6. **Document Exceptions**
   Track which controls are skipped in containers and ensure compensating controls exist.

Troubleshooting
---------------

**Playbook fails with "systemd not detected"**

This is expected in containers without systemd. Set:

.. code-block:: yaml

   is_container: true

**Audit shows many failures for kernel controls**

Container audits will fail kernel-related checks by design. Filter results:

.. code-block:: console

   # Filter out expected container failures
   cat audit_output.json | jq '.results[] | select(.skipped != true)'

**Permission denied errors**

Containers may need elevated privileges for certain audits:

.. code-block:: console

   docker run --privileged --pid=host your-audit-image

.. note::

   Running privileged containers should only be done in controlled environments
   for auditing purposes.
