============
Features
============

.. contents::
   :local:
   :depth: 2

❓What Are Feature Files?
==========================
A feature file contains one or more scenarios that instruct Behave which steps to run and in what order. 
Features are written in plain, human-readable language which is one of the things that makes Behave so powerful.

A standard feature file will begin with a description of what the feature is supposed to achieve. 
Feature files are often written using the user story style:

As a... -> I want... -> So that

*NOTE: It's entirely up to the user to write feature descriptions that are clear.
Although the following example is good practice, writing a description in a different way won't prevent the test from running.* 

Features are then broken down into scenarios where we can once again use the format 

Given -> When -> Then

A scenario may pass variables (such as username and password) to steps. 
These values can come from literals, environment variables, or secrets handled inside your step logic.

Feature files are the only place where you define multiple input sets using a Scenario Outline. (we'll talk more about this further down the page)

Using an outline can allow the test or, at a more atomic level, test steps to run several times using a variety of values.

.. dropdown:: 🌍 Real-world Analogy: (Click to expand)

   Imagine a Warehouse (again)

   In our warehouse analogy, the **Feature file** is the *blueprint* that
   defines what the entire operation is trying to achieve.

   - **Pages** are the workers who perform small, repeatable tasks.  
   - **Actions** are the floor manager who organises those tasks.  
   - **Steps** are the CEO who decides which workflow to run and under what conditions.  
   - **But the Feature file?**  
     It's the **master plan** the CEO reads from.

   A Feature describes:

   - the goal of the test  
   - why it matters  
   - the scenarios (chapters) that outline the sequence of actions  
   - any data sets to test (via Scenario Outlines)

   The Feature doesn't touch any machinery or make decisions.
   It simply tells the CEO:

   - *What* journey to follow  
   - *In what order*  
   - *With what data*

   In short:

   **Feature → Steps → Actions → Pages → WebDriver**  
   **Story → Decide → Organise → Do → Execute**


📍 Feature File Locations
==========================
Feature files are always stored in the ``features/`` directory and have the file extension ``.feature``. 

This is where Behave will look when running any scenarios. 

To keep it clean, ArgoBEAST automatically creates the ``features/`` directory and a sub directory ``steps``

Since the ``Steps`` you use in your scenarios will directly reflect the annotation given to a ``Step``, it's important you know where to look. 

🗺️ Features Responsibilities
=============================
What they should do
-----------------
- Clearly describe what you are trying to test
- Declare the values of variables 
- Declare multiple input sets using ``Scenario Outline``
- Invoke ``Steps`` in the correct order to achieve the test 

What they should not do
---------------------  
- There is no "code" in a feature file (Though comments are allowed and certainly recommended)
- Features will not interact with anything beyond ``Steps`` (i.e. you cannot call a PageAction from a feature)
- Do Not call driver methods
- Do Not call locators
- Do Not call BasePage methods

🎨 Creating a New Features file
===============================
To initialise a new Features file, you can use the ArgoBEAST CLI:

``argobeast create feature <name>``

This generates the basic scaffolding for a new feature file.

Since ``Features`` aren't inherently linked to one ``Page`` the name of the feature file should summarise what it's trying to achieve. 

for example:

.. code-block:: text

   login_feature.feature

Don't worry about including `_feature` ArgoBEAST will deal with that part for you.

An example of a feature file that continues our theme of logging in is below.

.. code-block:: Gherkin

   Feature: As a user, I want to log in to the application

   Scenario: Successfully log in as a user 
      Given I am on the login page
      When I log in using correct_username and correct_password
      Then I should see the home page welcome message

   Scenario: Unsuccessfully attempt to log in as a user 
      Given I am on the login page
      When I login using wrong_username and wrong_password
      Then I should see the unable to login message

If we want to take this further, we can create the scenarios as an outline and use multiple input values declared in a table. 

.. code-block:: Gherkin
   
   Scenario Outline: Successfully log in as a user 
      Given I am on the login page
      When I log in using <username> and <password>
      Then I should see the home page welcome message

    Examples: Users
      | username   | password     |
      | argobeast  | sup3rs3cr3t! |
      | argoadmin  | password123! |

The above example will run the same scenario twice inserting the values from the table. 

📝 Writing Scenarios
====================
First - let's establish the difference between a ``Feature`` and a ``Scenario``

**Features** - Describe what we're trying to test and provide a "home" for the scenarios that will get us there. 
**Scenarios** - Decide the order ``Steps`` should be run to test the ``Feature`` Description from all angles. 

When writing a ``Feature`` file, you should ensure you test both `happy` and `unhappy` paths.

The following examples are taken directly from the official Behave documentation which it's recommended to bookmark and refer to regularly:
https://behave.readthedocs.io/en/latest/

.. code-block:: Gherkin

   Feature: Fight or flight
   In order to increase the ninja survival rate,
   As a ninja commander
   I want my ninjas to decide whether to take on an
   opponent based on their skill levels

   Scenario: Weaker opponent
      Given the ninja has a third level black-belt
      When attacked by a samurai
      Then the ninja should engage the opponent

   Scenario: Stronger opponent
      Given the ninja has a third level black-belt
      When attacked by Chuck Norris
      Then the ninja should run for his life

🔗 Linking Steps to Features
=============================
It's important to remember that what you write in your ``Scenarios`` needs to match how it's written in the step you're trying to invoke. 

If you write:

``Given I am on the login page``

Then a step **MUST** exist that has the tag:

``@given("I am on the login page")``

Another important thing to note is that no two steps can have the same description. However, to assist with readability, it is possible to assign multiple tags to one step.

``@then("I click on the burger menu")``
``@then("I open the burger menu")``

This is perfectly acceptable and sometimes makes the scenario read better. Watch out though, if you are using paramaters the signatures must match on both. 

TL;DR
=====
``Features`` are a list of instructions that invoke steps. 
They do not **DO** anything, they simply declare what steps should be invoked, in what order and with what arguments. 