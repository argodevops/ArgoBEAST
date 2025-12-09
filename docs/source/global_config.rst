Global Configuration & Custom Context
=====================================

ArgoBEAST automatically loads the contents of your ``driver.yml`` file during the ``before_all`` hook. While this primarily handles browser and environment setup, it is also exposed globally to the test execution context.

This means ``driver.yml`` can serve as a persistent storage engine for your own custom test data, file paths, or credentials.

How it Works
------------

When the test run initiates, ArgoBEAST parses the YAML file and attaches the dictionary to ``context.beast_config``. This dictionary is accessible across all feature files, steps, and hooks.

Usage Example
-------------

1. **Define your data in ``driver.yml``**

   You can add arbitrary keys to your configuration file. These do not affect the internal driver setup unless they overwrite reserved ArgoBEAST keys.

   .. code-block:: yaml

       # driver.yml
       browser: chrome
       headless: true
       
       # Your custom data
       test_data:
         upload_path: "./data/uploads/"
         default_user: "admin_01"
         api_endpoint: "https://api.staging.example.com"

2. **Access the data in your Steps**

   You can retrieve these values anywhere the ``context`` object is available using standard dictionary methods.

   .. code-block:: python

       @step('I retrieve the test configuration')
       def step_impl(context):
           # Accessing the dictionary directly
           config = context.beast_config
           
           # safely get a custom variable
           upload_path = config.get("test_data", {}).get("upload_path")
           
           # Use the data in your logic
           print(f"Uploading files from: {upload_path}")

.. note::
   
   Using ``.get()`` is recommended over bracket notation (e.g., ``config['key']``) to prevent `KeyError` exceptions if a specific configuration value is missing from the environment.