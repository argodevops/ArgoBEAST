Chapter 2 - Initiating a Project
================================

Now you've installed ArgoBEAST you're ready to start writing your first test. 

1. Start by opening a terminal and running.

.. code-block:: bash

    argobeast init

You will be asked if you want to include example files. For this tutorial, please select no as we'll be creating them ourselves as we go. 

You will also be asked if you would like to attempt to install the required dependencies - it's recommended you select yes.

2. You should now have the following file structure:

.. code-block:: bash

   .
   ├── actions
   ├── config
   │   └── driver.yml
   ├── features
   │   ├── _common
   │   ├── environment.py
   │   └── steps
   ├── pages
   └── requirements.txt

Directory Breakdown
-------------------

- **actions**: This is where your actions files will be stored.
- **config/driver.yml**: This is the key file that will allow you to configure your webdriver along with many other settings. We'll go through these settings later.
- **features**: Feature files will be stored at the root of this directory.
- **features/_common**: This is where "magic hooks" are kept. We won't cover the in this tutorial but more information can be found under advanced features
- **features/environment.py**: Behave requires this file to run. The heavy lifting has been included in the ArgoBEAST framework but for Behave to remain happy, it needs to be able to see the environment.py file. Do not touch this. 
- **features/steps**: Steps files will be stored here. 
- **pages**: Pages files will be stored here.
- **requirements.txt**: This lists the versions of selenium and behave currently used by ArgoBEAST. 




