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

Form Population Engine
======================

ArgoBEAST includes a robust **Form Engine** designed to handle complex forms with minimal boilerplate code. Instead of writing unique logic for every form, you map the fields once and use a generic engine to drive the interactions.

The Workflow
------------

Populating a form requires four components working in harmony:

1.  **The Feature:** Defines *What* data to enter.
2.  **The Step:** Passes the data to the Action layer.
3.  **The Action:** Selects the correct Map and calls the generic engine.
4.  **The Page:** Defines the Map (Locators & Input Types).

1. The Feature File (The Tester)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Testers define the data using a vertical Data Table. You do not need to specify *how* to fill the field (e.g., dropdown vs text), only the value.

.. code-block:: gherkin

    Scenario: Create a new user
      Given I am on the registration page
      When I populate the registration form with:
        | Name           | Alice Bobson |
        | Role           | Administrator|
        | Active         | True         |
        | Gender         | Female       |
      And I click save

2. The Step Definition (The Router)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The step definition is extremely thin. It simply passes the raw Behave table to the specific action wrapper.

.. code-block:: python

    @when("I populate the registration form with")
    def step_impl(context):
        # Pass the generic Behave table directly to the action
        context.app.user_actions.populate_registration(context.table)

3. The Action Wrapper (The Configuration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Action class binds the **Data** (from the step) to the **Map** (from the page). It uses the ``populate_generic_form`` method available in ``BaseAction``.

.. code-block:: python

    class UserActions(BaseAction):

        def populate_registration(self, table_data):
            # 1. Select the specific map for this form
            target_map = self.page.REGISTRATION_MAP
            
            # 2. Call the generic engine
            self.populate_generic_form(target_map, table_data)

4. The Page Object (The Map)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is where the magic happens. The developer defines a dictionary mapping the "English Name" of the field to its **Locator** and **Input Type**.

**Syntax:** ``"Field Name": (Locator, InputType)``

.. code-block:: python

    class UserPage(BasePage):
        
        # Locators
        NAME_LOC = (By.ID, "user_name")
        ROLE_LOC = (By.ID, "role_select")
        ACTIVE_LOC = (By.ID, "is_active")
        GENDER_CONTAINER = (By.ID, "gender_options")

        # The Form Map
        REGISTRATION_MAP = {
            "Name":   (NAME_LOC, "text"),          # Standard Text
            "Role":   (ROLE_LOC, "select"),        # Dropdown
            "Active": (ACTIVE_LOC, "checkbox"),    # Checkbox (True/False)
            "Gender": (GENDER_CONTAINER, "radio_group") # Radio Group
        }

Supported Input Types
---------------------

The generic engine supports the following input types:

* ``"text"`` (Default): Clears the field and types the value.
* ``"select"``: Selects from a standard dropdown by visible text (falls back to value).
* ``"checkbox"``: Toggles the box to match the boolean string (e.g., "True", "Yes", "On").
* ``"radio"``: Clicks the specific element defined in the locator.
* ``"radio_group"``: Searches inside the container for a label or value matching the input string.
* ``"combobox"``: Handles Autocomplete/Streamlit inputs (Clear -> Type -> Enter