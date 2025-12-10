Allure Reporting Integration
============================

ArgoBEAST includes native support for **Allure**, an industry-standard reporting framework.

Enable Reporting
----------------

To enable Allure, simply add the following flag to your ``driver.yml``:

.. code-block:: yaml

    # driver.yml
    allure_reporting: true

This will automatically output results to the standard ``./allure-results`` directory.

Prerequisites
-------------

You must ensure the adapter library is installed:

.. code-block:: bash

    pip install allure-behave

HTML Report Generation
----------------------

ArgoBEAST attempts to **automatically generate** the HTML dashboard at the end of the test run.

* **Output Folder:** ``./allure-report``
* **Archive:** ``./allure-report.zip``

**Requirements:**
To use auto-generation, you must have the **Allure Commandline Tool** installed. If the tool is missing, ArgoBEAST will skip this step gracefully, saving only the raw data.

Installing The Allure Commandline Tool
--------------------------------------

Node

.. code-block:: bash

    npm install -g allure-commandline

Windows (Using scoop)

.. code-block:: bash

    scoop install allure

Mac (using Homebrew)

.. code-block:: bash
    
    brew install allure

Linux (Debian or Ubuntu)

.. code-block:: bash

    sudo apt-add-repository ppa:qameta/allure
    sudo apt-get update 
    sudo apt-get install allure