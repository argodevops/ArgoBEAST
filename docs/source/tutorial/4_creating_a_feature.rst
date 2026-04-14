Chapter 4 - Creating a feature
==============================

The feature files use Gherkin syntax (Given, When, Then) and essentially explain your tests in a human readable format.

More information can be found in the features portion of this documentation. 

1. Create a new feature file called `find chris tutorial` using the built in CLI command

.. code-block:: bash

   argobeast create feature "find chris tutorial"

You'll see a new file appear in the features directory. Open it and update the code as follows:

.. code-block:: feature

    Feature: Find_chris_tutorial

    Scenario: Example Find_chris_tutorial scenario
        Given I am on the argo home page
        When I navigate to About Us
        Then I can find chris

Each line in the feature file will relate to a step. Writing the feature file first makes it much easier to build tests as you can define what you're trying to achieve straight away.


