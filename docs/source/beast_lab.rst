
========================
The ArgoBEAST Lab (BETA)
========================

The **ArgoBEAST Lab** is a standardised, containerised testing environment. It provides a consistent execution space that includes a **Selenium Grid** and a dedicated **ArgoBEAST Runner**.

This is the recommended way to run tests in environments like **WSL2**, **GitPod**, or **CI/CD pipelines** where local browser management is often problematic.

Commands Overview
=================

+---------------------------+---------------+------------------------------------------------------------+
| Command                   | Action        | Description                                                |
+===========================+===============+============================================================+
| ``argobeast build lab``   | **Construct** | Generates the Docker infrastructure and local directory.    |
+---------------------------+---------------+------------------------------------------------------------+
| ``argobeast open lab``    | **Enter** | Boots the Selenium Grid, updates config, and enters shell. |
+---------------------------+---------------+------------------------------------------------------------+
| ``argobeast close lab``   | **Sanitise** | Shuts down the environment and frees up system resources.   |
+---------------------------+---------------+------------------------------------------------------------+

1. argobeast build lab
======================

This command prepares the physical "equipment" for your testing environment. It creates a dedicated ``argobeast_lab/`` directory in your project root.

* **Infrastructure**: Generates a custom ``argobeast.dockerfile`` and ``argobeast.dockercompose.yml``.
* **Isolation**: Uses a **Debian-slim** base to ensure compatibility across WSL, Linux, and Mac.
* **Persistence**: The Lab is built with an ``argouser`` to prevent file permission issues on your host machine.

.. note::
   Run this once per project, or whenever you need to reset your Lab equipment.

2. argobeast open lab
=====================

The primary gateway to your execution environment. When you run this command, ArgoBEAST performs a "System Pre-flight Check":

#. **Integrity Check**: Ensures Lab files exist.
#. **Config Sync**: Automatically scans your ``config/driver.yml``. If ``remote_url`` is missing or commented out, the Lab will wire it up for you.
#. **Engine Start**: Spins up a **Standalone Chrome** container and the **ArgoBEAST Runner**.
#. **Infiltration**: Executes an interactive session, placing you at the prompt: ``[argobeast lab]: /app #``

**Inside the Lab:**

Once the doors swing open, you are in a pure Python environment. Simply run:

.. code-block:: bash

   behave

to execute your tests. The Lab's internal network allows seamless communication with the Selenium Grid, so your tests will run as if they were on a local machine.

You can run any argobeast command from within the lab, but remember that the Lab is designed to be a self-contained environment. If you need to make changes to your host machine's configuration or files, exit the Lab first with:

.. code-block:: bash

   exit

3. argobeast close lab
======================

When testing is complete, use this command to "turn off the lights." It performs a ``docker compose down``, ensuring no orphaned containers are eating your RAM.

.. warning::
   For safety, you cannot close the Lab from *inside* the Lab. Type ``exit`` to return to your host machine first.

Technical Specifications
========================

The Selenium Grid (VNC)
-----------------------

The Lab includes a built-in "Observation Window." While the Lab is open, you can watch your tests execute in real-time:

* **URL**: ``http://localhost:7900``
* **Features**: Live browser interaction and debugging via NoVNC.

Environment Variables
---------------------

The Lab injects the following into your session:

* ``IS_IN_LAB=True``: Used by the framework to prevent recursive loops.
* ``ARGO_ENV=container``: Can be used in your code to toggle specific behaviors.
* ``SE_REMOTE_URL``: Pre-configured to point to the internal Grid service.

Troubleshooting
===============

"The Lab is Locked" (Permission Denied)
---------------------------------------

If you encounter a Docker socket error on Linux/WSL, your user needs permission to handle the equipment. Run:

.. code-block:: bash

   sudo usermod -aG docker $USER
   newgrp docker

"Missing Requirements"
----------------------

The Lab attempts to install your host's ``requirements.txt`` upon build. If you add new dependencies to your project, you must run ``argobeast build lab`` again to "restock" the Lab's libraries.
