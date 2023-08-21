Audit - FAQ
===========

Why does goss run manually fail?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

example.

.. code-block:: bash

   goss -g goss.yml -v

Goss is designed to run from the scripts passing discovered variables into Goss for metadata. Without these values being set, Goss will fail. These metadata variables can bee seen towards the end of the goss.yml file. With the run_audit script showing how these variables are created and passed to Goss.

