==========
Steps
==========

.. contents::
   :local:
   :depth: 2

❓What Are Steps?
===================
Steps are the detailed instructions that invoke actions, they are the only place where we should find conditional logic such as *If admin... else*.

They follow the format:

.. code-block:: Gherkin

   Given I do something
   When Something else
   Then I get this outcome

Behave offers annotations to describe what type of instruction the step is. For example. 

.. code-block:: python

   # login_steps.py
   @given("I am on the login page")
   def step_go_to_page(context):
       actions = context.app.get_actions(LoginActions)
       actions.go_to_page()

   @when("I log in using {username} and {password}")
   def step_example_action(context,username, password):
      actions = context.app.get_actions(LoginActions)
      actions.log_in(username, password)
   
   # home_steps.py
   @then("I should see the home page welcome message")
   def step_assert_result(context):
      actions = context.app.get_actions(HomeActions)
      home = actions.get_home_page_welcome_message()
      assert home == "Welcome to the Home Page!"
      

This follows the usual format of a feature (we'll cover feature files later on). 


.. code-block:: Gherkin

   Scenario: login to application

      Given I am on the login page
      When I login using {{username}} and {{password}}
      Then I should see the home page welcome message

.. dropdown:: 🌍 Real-world Analogy (Click to expand)

   Imagine a warehouse.

   On the factory floor, the workers handle the physical tasks:
   stacking boxes, moving pallets, printing labels.
   These are your Pages — they perform small, precise, repeatable actions.

   Overseeing them is the factory floor manager.
   He doesn't touch the boxes himself — he just organises the order of operations:
   first stack, then label, then move.
   That's your Actions layer.

   But above all of this is the CEO.

   The CEO never steps foot onto the warehouse floor.
   He doesn't carry boxes, print labels, or organise workflows.
   Instead, he looks at the bigger picture:

   What are we trying to achieve right now?

   Which workflow needs to run?

   Which conditions determine which path we follow?

   Are we doing the basic flow, or do special cases apply?

   Should we use a particular user, role, or credential?

   The CEO makes the decisions, sets the conditions, and chooses the direction.
   Then he hands the workflow instruction sheet to the floor manager (Actions),
   who carries out the plan using the workers (Pages).

   The CEO would never say:
   "Move that box 2cm to the left.""
   That's far too low-level.
   But he might say:
   "If this shipment is fragile, adjust the process and use the special packaging line.""

   That's exactly what Steps do.

   Steps don't click buttons or type into fields.
   Steps decide which workflow should run, under what conditions, and with which data.
   They contain the business rules, special cases, and branching choices that determine
   which Action should be executed.

   The CEO sets the direction.
   The manager orchestrates the sequence.
   The workers perform the tasks.

   Steps → Actions → Pages
   Decide → Organise → Do

   That's the role of Steps in ArgoBEAST.

👣 Steps Responsibilities
===========================
What they should do
-------------------
- Break scenarios down into clear directives (Given, When, Then)
- Branching logic decisions to inform which Actions are invoked (*if user=="Admin" then navigate to admin_view else navigate to worker_view*)
- Decide values of variables that are passed to actions.
- Assert results (Steps are the only place you should do this, actions package the results of the Page UI Interactions and send them back to steps to decipher)

What they should not do
-----------------------  
- Make any assumptions about how the actions are carried out
- Interact with the WebDriver in any way
   - Do Not call driver methods
   - Do Not call locators
   - Do Not call BasePage methods

🎒 What Is BaseStepContext?
============================

``BaseStepContext`` acts like a **magic backpack** for your test steps.

When you write a Step (**Given / When / Then**), you need a way to trigger your automation logic without worrying about how objects are instantiated or how the WebDriver is managed. 

Instead of requiring manual setup, ``BaseStepContext`` provides a streamlined gateway to your test logic via the Actions layer:

.. code-block:: python

   context.app.get_actions(SomeActions)

How it works:
------------

* **Clean Steps:** You primarily interact with **Actions** classes. This keeps your step definitions focused on high-level behavior rather than technical implementation.
* **Automatic Page Handling:** You never need to explicitly call or manage Pages within your steps. Because your Pages derive from ``BasePage``, they automatically inherit the correct WebDriver and configuration context.
* **Seamless Integration:** When you request an ``Actions`` class through the context, ArgoBEAST ensures it is ready to communicate with the underlying Page objects immediately.

In short:
---------

* **Steps** describe *what* should happen.
* **Actions** define *how* it happens by interacting with the Page layer.
* **BaseStepContext** is the bridge that provides those Actions instantly.

It keeps your test code simple, tidy, and strictly focused on describing the user journey.

🎨 Creating a New Steps file
=============================
To initialise a new Steps file, you can use the ArgoBEAST CLI:

``argobeast create steps <name>``

This generates the basic scaffolding for a new steps file.

Although it's perfectly acceptable to have multiple steps files per page, the recommendation is that each page has one steps file.

You are not limited to how many times you can use the Given, When, Then directives. 

Furthermore, Behave offers other options such as ``@step`` this will work in any position. 

More information can be found in the Behave documentation 
https://behave.readthedocs.io/en/latest/. 

The template will assume the existence of the respective ActionsClass and import it automatically. Though you can of course import any other actions or pages you like.

| *NOTE: If you have not initialised the page and actions, the imports will fail*
| *NOTE: The generated steps file will include imports for the matching Page and Actions classes. If you change file or class names, update these imports manually.*

Example
-------

Below is a simple Steps page for our login screen. Notice how the ``@then`` has been omitted since this lives in ``home_steps.py``. 

.. code-block:: python

   from behave import given, when, then
   from argo_beast.base.base_step_context import BaseStepContext
   from actions.login_actions import LoginActions

   # Behave automatically injects `context`
   # BaseStepContext gives you .get_page() and .get_actions()

   @given("I am on the login page")
   def step_go_to_page(context):
       actions = context.app.get_actions(LoginActions)
       actions.go_to_page()

   @when("I log in using {username} and {password}")
   def step_example_action(context,username, password):
      actions = context.app.get_actions(LoginActions)
      actions.log_in(username, password)


TL;DR
=====

Steps are logical descriptions of what work needs to be carried out.
They don't do the work themselves, nor do they instruct the workers to how to do the work. 
They simply make logical decisions about how and when that work should be completed. 