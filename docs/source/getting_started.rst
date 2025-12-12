=================
Getting Started
=================

.. contents::
   :local:
   :depth: 2

Overview
========
ArgoBEAST provides a simple platform for building functional, smoke, regression, and integration tests.

As a Systems Tester, you will build out the functionality of your application using a Page Object Model (POM).
This is comprised of:

- Pages
- Actions
- Steps
- Features

You’ll find more information on each component throughout this documentation.

At the highest level are Features.
Features use Gherkin syntax, powered by Behave, to describe tests in a clear, human-readable format.

.. admonition:: Example Feature

   | Feature: showing off behave
   |
   |    Scenario: run a simple test
   |       Given we have behave installed
   |       When we implement a test
   |       Then behave will test it for us!


Once the core functionality has been built, creating new tests becomes quick and straightforward for anyone.

Installation
============
Before you can start a new project, you will need to install ArgoBEAST.

You can do this with the whl file (instructions on how to generate a new whl file can be found in the README.md)

Once you have the whl file in an accessible location run: 

``pip install argobeast-x.x.x-py3-none-any.whl``

NOTE: The name of the whl file may vary depending on version. You will need to replace ``x.x.x`` with the current version. 

To confirm installation has been successful, you can run. 

``argobeast hello``

This should display a welcome message. 

     ### Welcome to ArgoBEAST! ###


Project Initialisation
======================
To start a new project run:

``argobeast init``

This will create the directories and files you will need to get started. 
You will be asked during initiation if you'd like example files to get you started. 
This will produce the following file structure.
:: 
   my-tests/
   │
   ├── pages/
   │   └── login_page.py
   ├── actions/
   │   └── login_actions.py
   ├── features/
   │   ├── login.feature
   │   └── steps/
   │       └── login_steps.py
   ├── config/
   │   └── driver.yml
   └── features/environment.py   
   
Behave discovers environment.py automatically, this contains logic for before, during and after tests. You should not touch this file. 

Creating a Brand New Page Collection
====================================

Many times, especially for a new testing suite, you'll need to create the Steps, Actions, and Page files for a new section of the system under test. 
Rather than creating each page individually, you can simply use the ArgoBEAST CLI to create all 3 files. 

``argobeast create all <name>``

Configuration
=============
| The file you'll need to check is ``config/driver.yml``.
| This contains configuration for the WebDriver such as:
|
| - Browser (Currently the only supported browser is Chrome)
| - Base URL (This is where your app is hosted)
| - WebDriver Wait: (This is the default wait time for the webdriver, used when searching for locators or waiting for the page to render.)
|
| The driver.yml is not an exhaustive list of options. The Selenium Documentation will help if you need to add more https://www.selenium.dev/documentation/webdriver/browsers/chrome/
| You can also override the config using a .env file or standard environment variables. 


Next Steps
==========
| Congratulations! Now you have everything you need to start writing tests. 
|
| Move on to the next section to start learning about the POM!

.. button-link:: pages
   :type: next
   :text: Next → Pages