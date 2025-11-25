========
Pages
========

.. contents::
   :local:
   :depth: 2

❓What Are Pages?
===============
Pages are low level wrappers for locators and basic UI interactions. 
They should not contain any complex logic about how the functionality works - they simply "paint the picture" by providing interactions for the actions page to utilise. 

💡 Why this matters

Pages should be dumb. They describe what elements exist and how to interact with them, nothing else.

Actions should be smart. They orchestrate multi-step flows and business logic.

.. dropdown:: 🌍 Real-world Analogy (Click to expand)
   
   Imagine a warehouse.

   A factory worker spends all day stacking boxes.
   At the start of the shift, the manager tells him how many boxes to stack and how high each stack should be.

   If the manager says “I need 5 stacks of 5 boxes,” the worker simply builds:

   - 5 stacks

   - Each 5 boxes high

   He doesn't decide why this needs doing or when, he just performs the physical action repeatedly and reliably.

   Now imagine a second factory worker whose job is to label the boxes.
   The manager tells her what each label should say, and she gets on with it.
   Again, she doesn't decide if the labels are correct, important, or part of a bigger workflow.

   The two factory workers never communicate with each other.
   They just perform their individual tasks in isolation.

   The manager is the one orchestrating everything - 
   assigning tasks, deciding the order, and ensuring the workflow makes sense.

   🧠 How This Maps to ArgoBEAST

   To put the analogy into the context of ArgoBEAST:

   - Pages = The factory workers
   They perform small, precise, repeatable tasks like clicking a button, typing into a field, or reading text.
   They don’t know anything about the bigger workflow.

   - Actions = The manager
   This is where the logic lives — deciding what should happen and in what order.
   Actions tell Pages which tasks to perform and when.

   - Steps = The instructions given to the manager
   Steps are written in plain English (Given/When/Then).
   They describe what should happen from the tester's perspective.
   Steps call Actions, and Actions call Pages.

   - Features = The high-level test script
   This is the overall scenario or test case written in Gherkin, describing the behaviour you want to validate.

   | ``Feature  →  Steps  →  Actions  →  Pages  →  WebDriver``
   | ``(What)      (Describe) (Decide)    (Do)      (Execute)``

📜 Page Responsibilities
=====================
What it should do
----------------
- Specify the locators (fields that need to be populated)
- It will accept the string values to use
- It will populate the locators with the correct values. 

What it should not do
---------------------  

- Contain logic that decides when or why a field should be populated
- Validate business rules (e.g., “if login fails, try again”)
- Trigger navigation flow (e.g., moving from login → dashboard)
- Perform multi-step workflows
- Compare expected vs. actual results
- Make assertions
- Contain conditional logic based on test scenarios
- Handle test data or scenario-specific values
- Decide which user role, state, backend condition, or branch to follow


🎨 Creating a Page
==================

To initialise a new Page, you can use the ArgoBEAST CLI:

``argobeast create page <name>``

This generates the basic scaffolding for a new Page class.

At the top of the class (inside ``__init__``), you add your **locators**.
Some POM models put locators in a separate file, but ArgoBEAST keeps them inside the Page for clarity and simplicity.

From here, a Page should define **only low-level interactions**, such as typing into a field or clicking a single button.
A Page should *not* contain multi-step flows — that belongs in the Actions layer.

Example
-------

Below is a simple Page definition for a login screen.
Notice how each method performs **one** UI action and nothing more.

.. code-block:: python

    class LoginPage(BasePage):
        def __init__(self, driver, config):
            super().__init__(driver, config)
            self.USERNAME = ("id", "username-input")
            self.PASSWORD = ("id", "password-input")
            self.SUBMIT   = ("id", "submit-btn")

        def enter_username(self, value):
            return self.type_text(self.USERNAME, value)

        def enter_password(self, value):
            return self.type_text(self.PASSWORD, value)

        def click_submit(self):
            return self.click(self.SUBMIT)

Each method does exactly **one** thing:

- ``enter_username()`` → types into the username field  
- ``enter_password()`` → types into the password field  
- ``click_submit()`` → clicks the button

No branching logic.  
No ``if`` / ``else``.  
No multi-step workflows.

Exactly the kind of “dumb” behaviour Pages should have.

❓ Why not add a ``populate_login_form()`` method here?
------------------------------------------------------

Great question! everyone asks this at some point.

You *could* write something like:

.. code-block:: python

    def populate_login_form(self, username, password):
        self.enter_username(username)
        self.enter_password(password)

But this is **no longer a single UI action** — it’s a **mini workflow**.
Even though it's small, it represents a *sequence* of steps, which is the responsibility of the **Actions** layer.

Why?

- Actions orchestrate *flows*  
- Pages expose only the *tools* needed for those flows

So instead, the **Actions** file would contain:

.. code-block:: python

    def login(self, username, password):
        self.page.enter_username(username)
        self.page.enter_password(password)
        self.page.click_submit()

This keeps the architecture clean:

``Page   = how to type/click``  
``Action = when and why to do it``

And this separation becomes incredibly important as your application grows.

🧩 Summary
----------

- Pages define **locators**
- Pages implement **single UI actions**
- Actions implement **workflows** that combine those actions
- Steps call Actions
- Features describe behaviour

This structure keeps your tests readable, predictable, and easy to maintain no matter how large the application becomes.


TL;DR
======

A page class lists all of the elements on the page and small methods describing how you would interact with each. 

Some elements have more than one UI interaction that can be performed, for instance, click + type

If both UI Interactions are required then there should be one method written for each. 


Working With BasePage
=====================
Each page uses the BasePage. This is where ArgoBEAST really benefits the user. 

BasePage contains methods for most of the common actions a user might perform on a locator.

These are the methods that should be used, individual pages should not be responsible for any new WebDriver logic. 

.. dropdown:: Available Base Page UI Interactions (Click to Expand)

   .. automodule:: test_framework.base.base_page
      :members:
      :undoc-members:
      :show-inheritance:
