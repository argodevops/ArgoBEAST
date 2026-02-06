ArgoBEAST Configuration Guide
=============================

ArgoBEAST is controlled via the user configuration file, typically named ``driver.yml``.

While the framework comes with internal defaults, ``driver.yml`` is where you define your specific project settings, such as browser choice, timeouts, and reporting preferences.

Configuration File Location
---------------------------

By default, ArgoBEAST looks for your configuration file at:

``config/driver.yml``

Custom Config Paths (CI/CD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to store your configuration elsewhere (or if you want to swap configurations dynamically in a CI pipeline), you can override the default path using the ``TEST_CONFIG`` environment variable.

**Example (Linux/Mac):**

.. code-block:: bash

   export TEST_CONFIG="my_custom_configs/staging_config.yml"
   behave

**Example (Windows PowerShell):**

.. code-block:: powershell

   $env:TEST_CONFIG="my_custom_configs/staging_config.yml"
   behave

Webdriver Configuration
-----------------------

These settings control the instantiation of the browser session.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Key
     - Description
     - Options / Notes
   * - **browser**
     - The browser to run tests on.
     - ``chrome``, ``firefox``, ``edge`` (Case insensitive)
   * - **driver_path**
     - The path to your WebDriver executable (e.g., chromedriver.exe).
     - Required if not using Selenium Manager. Can be left empty if using Selenium Manager or if the driver is in your system PATH.
   * - **headless**
     - Runs the browser without a visible UI. Recommended for CI/Docker.
     - ``true`` / ``false``
   * - **window_size**
     - Sets the initial viewport dimensions.
     - Format: ``"WIDTH,HEIGHT"`` (e.g., ``"1920,1080"``).
       *Note: This works universally across all supported browsers in both Headless and Headful modes.*
   * - **remote_url**
     - The URL for a Selenium Grid or Docker container.
     - Leave empty ``""`` for local execution.

Advanced: Browser Arguments (browser_args)
------------------------------------------

ArgoBEAST allows you to pass custom flags directly to the browser options at startup. This provides flexibility for specific testing needs (e.g., testing incognito mode, handling SSL errors, or performance profiling).

.. warning::
    **ArgoBEAST does not validate these flags.**

    We simply pass them to the underlying driver. It is your responsibility to ensure the flags you provide are compatible with the browser you selected.

How to use
~~~~~~~~~~

Uncomment the ``browser_args`` section in your ``driver.yml`` file and add your flags as a list.

**Example: Chrome / Edge**

.. code-block:: yaml

    browser: chrome
    browser_args:
      - "--incognito"
      - "--disable-gpu"
      - "--ignore-certificate-errors"

**Example: Firefox**

.. code-block:: yaml

    browser: firefox
    browser_args:
      - "--private"
      - "--allow-downgrade"

*Note: If you provide a Chrome-specific flag (like ``--disable-extensions``) while running Firefox, the driver may ignore it or fail to start. Check the official driver documentation for valid arguments.*

Timeouts & Stability
--------------------

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Key
     - Description
     - Recommended
   * - **implicit_wait**
     - Global fallback wait time (in seconds) for finding elements.
     - ``5`` (Keep low if using Explicit Waits)
   * - **explicit_wait**
     - The standard timeout used by ``CommonActions`` for dynamic elements.
     - ``10`` - ``15``
   * - **page_load_timeout**
     - Maximum time to wait for a page to fully render before throwing an error.
     - ``30``+ (Increase for heavy apps)

Application Settings
--------------------

* **base_url**:
  The entry point for your tests (e.g., ``http://localhost:8501``).

* **default_route**:
  The default path appended to the base URL during the initial navigation step (usually ``/``).

Framework Behaviour
-------------------

* **screenshot_on_failure**:
  If ``true``, a screenshot will be captured automatically when a step fails.

* **output_directory**:
  The folder where failed screenshots and other artifacts are saved.

* **retry_failed_scenarios**:
  *(Experimental)* If ``true``, the framework attempts to re-run fragile scenarios. Default is ``false``.

* **max_retries**:
    *(Experimental)* The maximum number of retry attempts for failed scenarios when ``retry_failed_scenarios`` is enabled. Default is ``2``.
----------------

ArgoBEAST has built-in integration for Allure, provided you have the ``allure`` command-line tool installed on your machine.

* **allure_reporting**:
  Main switch. Set to ``true`` to generate JSON results in ``allure-results``.

* **hide_skipped_tests**:
  If ``true``, scenarios marked with ``@skip`` are excluded from the final report entirely.

* **auto_generate_report**:
  If ``true``, ArgoBEAST will attempt to run ``allure generate`` at the end of the test run and bundle the HTML into a ZIP file.

  .. note::
     The ``allure`` binary must be in your system PATH for this to work.

* **allure_keep_history**:
  If ``true``, copies history from previous runs to show trend graphs.

Logging
-------

* **log_level**:
  Controls the verbosity of the console output.

  * ``INFO``: Standard execution logs.
  * ``DEBUG``: Detailed logs for framework development/debugging.
  * ``ERROR``: Only show critical failures.