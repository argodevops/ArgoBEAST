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
* ``"combobox"``: Handles Autocomplete/Streamlit inputs (Clear -> Type -> Enter)