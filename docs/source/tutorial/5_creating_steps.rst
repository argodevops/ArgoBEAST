Chapter 5 - Creating Steps 
##########################

In the previous chapter, we created a feature file. This defined the steps that we'll need for the test to run. 

For this tutorial, the steps are intentionally vague and don't reflect the sort of test you'd expect to see in a "real" test suite. 

They have been written to give us an opportunity to explore the Page Object Model (POM) that ArgoBEAST uses.

1. Creating required steps files
********************************

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
   
   argobeast create steps about

2. Writing the Given step
*************************

- Open the file `features/steps/home_steps.py`

*NOTE*: There is an import for a file that doesn't exist `from actions.home_actions import HomeActions` don't panic - we'll create that in the next Chapter.

- Since we're only creating a given step, go ahead and delete the placeholder code for the `when` and the `then` steps. 

- You should now be left with the below:

.. code-block:: python

    from behave import given, when, then
    from actions.home_actions import HomeActions

    # Behave automatically injects `context`
    # BaseStepContext gives you .get_page() and .get_actions()

    @given("I am on the {name} page")
    def step_go_to_page(context, name):
        actions = context.app.get_actions(HomeActions)
        pass

You'll notice how the step is using a template for the page name. 

For this test we're going to hard code the page instead. 

Replace the `@given` block with:

.. code-block:: python
   
   @given("I am on the argo home page")
   def on_home_page(context):
       actions = context.app.get_actions(HomeActions)

- Next we'll add an assertion along with an expectation to confirm we're on the home page. add the following to the method.

.. code-block:: python

    expected_text = "Who We Are"
    screen_text = actions.get_home_text()
    assert screen_text == expected_text


The "Home Page" Dilemma
-----------------------

In this step, we are using the following Gherkin:

`Given I am on the argo home page`

In a standard automation suite, simply navigating to the URL is usually enough to "satisfy" this step. However, for the sake of this tutorial, we are going to add an Assertion to verify that a specific element (like the logo or page title) is visible before we proceed.

*A Note on Best Practices*
You might notice that we are "testing" inside a Given step. Generally, this is not considered best practice in production-grade testing for two reasons:

 - Intent vs. Verification: The Given step is meant to set the initial state (the "Context"). The Then step is where the actual verification (the "Outcome") should happen.

 - Brittle Setup: If your Home Page assertion fails, your entire test suite stops before it even begins. In large projects, we prefer to keep our setup steps as "lean" as possible to ensure that when a test fails, it's failing because of the specific feature under fire, not the setup.

Why are we doing it here?
-------------------------

Since this is our first interaction with the browser in this tutorial, we want to ensure everything is wired up correctly. It's a "smoke test" to confirm that ArgoBEAST has successfully launched the driver and reached the application before we move on to more complex interactions.


3. Writing the When Step
************************

The when step will complete an action. For our test, we're using a generic naviation action. 

- Open the file `features/steps/general_steps.py`

As before, there is an import that doesn't yet exist - ignore this for now. In this file, we're only going to create a `when` step so feel free to delete the `given` and `then` placeholders. 

- Update the `when` code to:

.. code-block:: python 
    
    @when("I navigate to {page}")
    def navigate_to_page(context, page):
        actions = context.app.get_actions(GeneralActions)
        actions.navigate_to_page(page)

You will notice that for this step, we're using templating. This allows us to reuse the same code for navigating to any page. 

The {page} placeholder in the step definition is passed as the page argument to the function. 

4. Writing the Then Step
************************

This is the epic conclusion of any test, it's crunch time. 

More often than not, we would make an assertion in the `then` to check a condition has been met. In our case - Can we see Chris?

- Open the file `features/steps/about_steps.py`

As in the previous 2 steps, ignore the non-existent import. We're focussing on the `then` so you can remove the `given` and `when` steps.

- Update the `then` code to:

.. code-block:: python
   
   @then("I should see Chris")
   def check_chris_visible(context):
       actions = context.app.get_actions(AboutActions)
       assert actions.is_chris_visible()
