Advanced Features
=================

The Common Library
------------------

ArgoBEAST includes a powerful "Macro" system that allows you to reuse Gherkin scenarios across your entire test suite without writing a single line of Python code.

We call this **The Common Library**.

The Problem
~~~~~~~~~~~

In standard BDD, you often find yourself repeating the same setup steps in every feature file:

.. code-block:: gherkin

    Given I navigate to the login page
    And I enter "admin" into the username field
    And I enter "password123" into the password field
    And I click the login button
    # ... finally, start the actual test ...

This violates the **DRY** (Don't Repeat Yourself) principle. If the login URL changes, you have to update dozens of feature files manually.

The Solution: Magic Hooks
~~~~~~~~~~~~~~~~~~~~~~~~~

ArgoBEAST allows you to define these steps **once** in a special library folder, and then "inject" them into any test using a simple tag.

How it Works
------------

1. The Library Folder
~~~~~~~~~~~~~~~~~~~~~

When you initialize a project using ``argobeast init``, the framework creates a special folder: ``features/_common``.

* **Definition:** Any feature file inside this folder is treated as a **Library**.
* **Behavior:** These files are **skipped** during normal test runs. They exist only to provide steps for other tests.

.. tip::
    The folder starts with an underscore (``_common``) to signify that it is a partial/dependency, similar to SCSS or private Python modules. This also keeps it sorted at the top of your file explorer.

2. Defining a Hook
~~~~~~~~~~~~~~~~~~

To create a reusable hook, simply write a standard Gherkin scenario inside the ``_common`` folder and give it a unique **@tag**.

**File:** ``features/_common/auth.feature``

.. code-block:: gherkin

    Feature: Authentication Library

      @login_admin
      Scenario: Standard Admin Login
        Given I navigate to the login page
        When I enter "admin" into the username field
        And I enter "password123" into the password field
        And I click the login button
        Then I should be on the dashboard

.. note::
    The tag (e.g., ``@login_admin``) acts as the unique ID for this macro.

3. Using the Hook (Setup & Teardown)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, in your real tests, you can trigger this macro using the prefixes ``@setup:`` or ``@teardown:``.

**File:** ``features/products.feature``

.. code-block:: gherkin

    Feature: Product Management

      @setup:login_admin
      Scenario: Create a new product
        Given I am on the products page
        When I click "New Product"
        # ... rest of your test

Execution Flow
--------------

#.  **@setup:** ArgoBEAST sees ``@setup:login_admin``. It pauses the test, looks up the ``@login_admin`` steps from the library, and runs them first. If the setup fails, the test fails immediately.
#.  **The Test:** Your scenario runs normally.
#.  **@teardown:** If you included a ``@teardown:`` tag, those steps run after your scenario finishes (even if the test failed), ensuring your environment is always left clean.

Rules & Best Practices
----------------------

Tag Placement
    * In the **Library** (``_common``), tags must be placed on the **Scenario**, not the Feature.
    * In your **Tests**, you can place ``@setup:`` tags on the **Scenario** (runs for that specific test) or the **Feature** (runs before every scenario in that file).

Naming Conventions
    * Use distinct names for your hooks (e.g., ``@login_admin``, ``@clean_db``).
    * If two hooks share the same name, ArgoBEAST will overwrite one with the other.

Testing Your Hooks
    Since library files are skipped by default, you might wonder how to verify they work. You can run them explicitly via the CLI:

    .. code-block:: bash

        behave features/_common/auth.feature

    ArgoBEAST detects the explicit path and allows the library file to execute as a normal test.

Example: Database Cleanup
-------------------------

A common pattern is to ensure a clean state before or after complex tests.

**Definition:** ``features/_common/data.feature``

.. code-block:: gherkin

    @clean_db
    Scenario: Truncate all user data
      Given I connect to the database
      And I execute "TRUNCATE users CASCADE"

**Usage:** ``features/registration.feature``

.. code-block:: gherkin

    @teardown:clean_db
    Scenario: Register a new user
      Given I sign up as "test_user"
      # ... assertions ...
      # The DB will be cleaned automatically after this test finishes.