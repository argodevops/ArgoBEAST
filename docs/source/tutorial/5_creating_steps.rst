Chapter 5 - Creating Steps 
==========================

In the previous chapter, we created a feature file. This defined the steps that we'll need for the test to run. 

For this tutorial, the steps are intentionally vague and don't reflect the sort of test you'd expect to see in a "real" test suite. 

They have been written to give us an opportunity to explore the Page Object Model (POM) that ArgoBEAST uses.

1. Creating required steps files
--------------------------------

**Given I am on the argo home page**

This directly relates to the home page so we will need to create a steps file for `home`

.. code-block:: bash

   argobeast create steps home

**When I navigate to About Us**

This step is more generic and doesn't directly relate to one single part of the website. For this reason, we're going to create a steps file for `general`

.. code-block:: bash

   argobeast create steps general

**Then I can find chris**

Finally, we have a step that relates to the `about us` page. 

.. code-block:: bash
   
   argobeast create steps about_us

2. Writing the Given step

