Troubleshooting & FAQ
====================

This page covers common issues encountered while setting up or running tests within the ArgoBEAST framework.

Browser & Environment Issues
----------------------------

Firefox on Ubuntu 24.04+ (Snap Sandboxing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:**
Tests fail to launch Firefox with errors such as ``Binary is not a Firefox executable``, ``Profile not found``, or ``WebDriverException: Service geckodriver unexpectedly exited``.

**Cause:**
Ubuntu 24.04 installs Firefox as a **Snap** package by default. Snap's strict security confinement prevents GeckoDriver from accessing the necessary system directories (like ``/tmp``) to initialise a testing profile.

**Resolution:**
To bypass the sandbox without uninstalling your system browser, instruct **Selenium Manager** to provision a standalone, non-sandboxed version of Firefox for automation.

Add this environment variable to your shell (e.g., ``~/.bashrc``) or your CI/CD environment:

.. code-block:: bash

   # Forces Selenium to download a managed browser binary to ~/.cache/selenium
   export SE_FORCE_BROWSER_DOWNLOAD=true

Distribution Compatibility (Mint, Debian, Arch)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On distributions where Firefox is installed via native package managers (like ``apt`` on Mint or ``pacman`` on Arch) rather than Snap, ArgoBEAST typically works without extra configuration. 

However, using ``SE_FORCE_BROWSER_DOWNLOAD=true`` is recommended for teams to ensure all contributors are running the exact same browser version regardless of their OS.

WebDriver Management
--------------------

Automatic Driver Provisioning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ArgoBEAST relies on **Selenium Manager** (built into Selenium 4.11+) to handle driver binaries. You generally do not need to manualy download ``chromedriver`` or ``geckodriver``.

If drivers fail to download:
* **Proxy Settings:** If you are behind a corporate firewall, ensure ``HTTP_PROXY`` and ``HTTPS_PROXY`` are set in your environment so the manager can reach the binary repositories.
* **Permissions:** Ensure the user running the tests has write access to the ``~/.cache/selenium`` directory.

Reporting & Execution
---------------------

Reports Not Generating
~~~~~~~~~~~~~~~~~~~~~~
ArgoBEAST uses **Allure** for test reporting. The logic for report generation is managed internally by the framework's core hooks. If your reports are not generating after a run, it is almost certainly due to missing dependencies.

**Resolution:**
1. **Check Allure Installation:** Ensure you have the Allure command-line tool installed on your system path.
   
   * On Ubuntu/Mint: ``sudo apt install allure`` (or via npm/homebrew).
   * Verify with: ``allure --version``.

2. **Python Dependency:** Ensure the ``allure-behave`` formatter is installed in your Python environment:
   
   .. code-block:: bash

      pip install allure-behave

    Or if using **uv** for dependency management:
    
   .. code-block:: bash
      
      uv add allure-behave

3. **Execution Command:** Ensure you are running your tests with the correct formatter flag to output the results to the results directory:

   .. code-block:: bash

      behave -f allure_behave.formatter:AllureFormatter -o %allure_result_folder%

*Note: If you are using the ArgoBEAST CLI to initiate runs, these flags are typically handled for you, provided Allure is present on the system.*

Standardising Team Environments
-------------------------------

To prevent "it works on my machine" issues across different Linux distributions, it is best practice to standardise the browser source. You can create a simple setup script for contributors:

.. code-block:: bash

   #!/bin/bash
   # Standardise ArgoBEAST environment
   export SE_FORCE_BROWSER_DOWNLOAD=true
   echo "Environment configured for ArgoBEAST."