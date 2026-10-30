Contributing
------------

Community contributions come through GitHub issues and pull requests. Each role and audit
repository carries a ``CONTRIBUTING.md`` with the full rules; the main points are:

- **Issues are open to everyone.** Include the branch you are on, your Ansible version, the
  control affected, and the actual against the expected behavior.
- **Pull requests come from approved contributors.** To become one, join the
  `Discord server <https://www.lockdownenterprise.com/discord>`_ and ask in the community channel,
  saying what you would like to work on. A maintainer will confirm no one is already working on it
  and walk you through the conventions.
- **Every commit must be GPG signed and carry a Signed-off-by line** (``git commit -S -s``).
- **Pull requests target the devel branch**, or a staging branch first when they come from a fork.
  Maintainers merge devel to main for each release.
- Respect the community's time and effort that goes into feedback and support.

.. toctree::
   :maxdepth: 3

   audit/audit_development.rst
   remediate/rem_development.rst
   combined/molecule-testing.rst
