Molecule - Linux-Based Container Testing
========================================

`Molecule <https://ansible.readthedocs.io/projects/molecule/>`_ is the framework used to
develop and test the Ansible Lockdown roles. It provisions a disposable target, applies the
role against it, and asserts the resulting system state. For the Lockdown roles the target is
a **Linux-based container** (Docker is the default driver; Podman also works), which makes the
scenarios fast to spin up and tear down and lets the same tests run locally and in CI.

Every remediation and audit role in the project ships a ``molecule/`` directory so
contributors can validate changes locally before opening a pull request, and so the same
scenarios can be exercised in the pipelines.

Two stages do most of the work:

- **converge** - run the role against the container target, exactly as a user would.
- **verify** - assert that the container reached the expected state after remediation.

.. note::

   Because the targets are Linux containers, container-detection facts are set and tasks
   guarded by ``when: not system_is_container`` are skipped. This keeps the scenarios light
   but means they do not exercise every code path - see `Platforms and ARM64`_ below.

Prerequisites
-------------

Molecule runs from a workstation with Python, Ansible, and a container runtime available.
Docker is the default driver used across the roles; Podman also works.

.. code-block:: console

   # Python tooling (a virtualenv is recommended)
   pip install molecule molecule-plugins[docker] ansible-core

   # A container runtime must be installed and running
   docker info

   # Confirm molecule sees the docker driver
   molecule --version

.. note::

   The container images a scenario uses are declared in each role's ``molecule/<scenario>/molecule.yml``
   and are aligned with the platforms listed in the role's ``meta/main.yml``. Use an image that
   matches the benchmark you are testing (for example a RHEL 9 image for ``RHEL9-CIS``).

Repository layout
-----------------

A role's Molecule configuration lives under ``molecule/`` with one directory per scenario.
Each scenario directory holds four files:

.. code-block:: text

   molecule/
   └── default/
       ├── molecule.yml     # driver, platform image(s), host_vars, and verifier
       ├── prepare.yml      # bootstrap the container (python + packages) before the role runs
       ├── converge.yml     # playbook that applies the role (sets required variables)
       └── verify.yml       # assertions run against the converged target

- **prepare.yml** brings a minimal container image up to a testable baseline: it bootstraps
  Python with ``ansible.builtin.raw`` (so Ansible can run at all), then installs the packages
  the benchmark expects to be present (for example auditd, aide, firewalld, and crypto-policies).
  Minimal images ship far fewer packages than a real host, so this step is what makes the
  role's tasks meaningful.
- **converge.yml** applies the role and sets the variables a container run needs -
  ``setup_audit: true`` and ``run_audit: true`` so the paired audit runs, plus container
  affordances such as ``system_is_container: true`` and ``skip_reboot: true``. It typically
  sets a root password in ``pre_tasks`` so PAM hardening does not lock the session out.
- **verify.yml** asserts the resulting state when the scenario's verifier is ``ansible``.

Scenarios let a single role be tested in more than one way. Coverage differs between the
CIS and STIG roles:

- **CIS operating-system roles** are the most consistent, typically shipping ``default``,
  ``localhost``, and ``wsl`` scenarios. ``RHEL9-CIS`` additionally provides a ``ubi`` scenario.
- **STIG operating-system roles** are generally thinner, shipping a ``default`` scenario;
  ``RHEL9-STIG`` also provides a ``ubi`` scenario.

Scenario configuration
----------------------

Because the roles harden systemd-managed services, the container must run a real init system.
A representative ``molecule.yml`` platform block (from ``RHEL9-CIS``) shows the settings that
make this work:

.. code-block:: yaml

   driver:
     name: docker
   platforms:
     - name: rhel9-cis-qa
       image: rockylinux/rockylinux:9-ubi-init   # an "-init" image that ships systemd
       command: /usr/sbin/init                   # PID 1 is systemd, not a shell
       pre_build_image: true
       privileged: true
       cgroupns_mode: host
       volumes:
         - /sys/fs/cgroup:/sys/fs/cgroup:rw
       tmpfs:
         - /run
         - /tmp
       capabilities:
         - SYS_ADMIN
   provisioner:
     name: ansible
     inventory:
       host_vars:
         rhel9-cis-qa:
           setup_audit: true
           run_audit: true
           system_is_container: true
           skip_reboot: true
   verifier:
     name: ansible

.. important::

   The ``-init`` image, ``command: /usr/sbin/init``, ``privileged: true``,
   ``cgroupns_mode: host``, the cgroup volume mount, and the ``/run`` + ``/tmp`` tmpfs mounts
   are all required for systemd - and therefore any service-oriented control - to work inside
   the container. Omitting them causes hard-to-diagnose failures in tasks that manage services.

.. note::

   Not every role uses ``verify.yml`` for assertions. The verifier is set by the scenario's
   ``molecule.yml`` ``verifier:`` key - ``RHEL9-CIS`` uses ``ansible`` with a ``verify.yml``,
   while some roles rely on the paired audit (Goss) profile as the verification step instead.
   Check the ``verifier`` setting and whether ``verify.yml`` is present before assuming a
   scenario asserts state on its own. Use an existing role such as ``RHEL9-CIS`` as a working
   reference when adding a new scenario.

Running tests
-------------

Run Molecule from the root of the role. A scenario other than ``default`` is selected with
``-s <scenario>``.

.. code-block:: console

   # Full lifecycle: create -> converge -> idempotence -> verify -> destroy
   molecule test

   # Iterating during development (leave the instance running):
   molecule create      # provision the target
   molecule converge    # apply the role
   molecule verify      # run the assertions
   molecule destroy     # tear the target down

   # Target a named scenario
   molecule test -s localhost

   # Shell into the running target to debug a failure
   molecule login

.. important::

   Always ``molecule destroy`` before re-running ``molecule converge`` to guarantee a clean
   target. Stale containers are a common cause of "instance is not running" style errors.

Idempotency
-----------

Remediation roles must be idempotent: a second run should change nothing. Molecule checks
this with the idempotence action, which runs ``converge`` a second time and fails if any task
reports a change.

.. code-block:: console

   molecule idempotence

   # or exercise it as part of the full lifecycle
   molecule test

If the second run reports changes, the offending tasks need ``changed_when`` corrected or the
remediation logic adjusted so it detects the already-compliant state. See the idempotency
guidance in the :doc:`remediation FAQ </remediate/rem-faq>` for common causes.

Linting integration
-------------------

Molecule is one layer of a wider quality gate. Pull requests are also expected to pass
``ansible-lint``, ``yamllint``, and the repository ``pre-commit`` hooks. Rather than duplicate
that guidance here, see the linting and standards sections of the
:doc:`remediation development guide </remediate/rem_development>` and the
:doc:`audit development guide </audit/audit_development>`.

Platforms and ARM64
-------------------

The platform images a scenario runs against are driven by the role's ``meta/main.yml`` and the
scenario ``molecule.yml``. Container-based scenarios behave differently from full virtual
machines in ways that affect testing:

- Container targets set container-detection facts, so tasks guarded by ``when: not system_is_container``
  are skipped. See the :doc:`container and Docker guide </container-guide>` for how this
  affects coverage.
- ARM64/aarch64 targets have auditd syscall differences that cause some audit assertions to
  behave differently than on x86_64. See the :doc:`ARM64 guide </arm64-guide>`.

.. important::

   Because container scenarios skip container-gated tasks, they do not exercise every code
   path. Where possible, complement Molecule container runs with testing on a full VM or a real
   CI runner so container-gated logic is also covered.

CI/CD pipelines
---------------

The same scenarios run in the project's GitHub Actions pipelines on pull requests, so a change
that passes locally with ``molecule test`` should also pass in CI. When CI fails but a local
Molecule run passes, suspect a difference in the test substrate (for example a missing package
or an unresolvable hostname on the CI image) rather than the role logic.

Troubleshooting
---------------

**Error:** ``instance is not running`` or a stale container is reused.

Run ``molecule destroy`` (or ``molecule reset``) and converge again from a clean state.

**Symptom:** Idempotence action fails on the second converge.

A task is reporting a change on an already-compliant system. Inspect the changed tasks in the
output and correct ``changed_when`` or the remediation condition.

**Symptom:** Audit/verify assertions fail only in a container or only on ARM64.

Expected for container-gated tasks and for auditd syscall differences on ARM64. Confirm against
the :doc:`container </container-guide>` and :doc:`ARM64 </arm64-guide>` guides before treating
it as a role defect.

Best Practices
--------------

1. **Start clean** - ``molecule destroy`` before each fresh ``converge``.
2. **Test idempotency** - a second converge must report zero changes.
3. **Match the image to the benchmark** - use an image for the OS/version the role targets.
4. **Do not rely on containers alone** - container-gated tasks are skipped; also test on a VM
   or CI runner where practical.
5. **Run the full gate** - pass ``ansible-lint``, ``yamllint``, and ``pre-commit`` alongside
   Molecule before opening a pull request.
