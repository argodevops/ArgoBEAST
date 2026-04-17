===========================
Cheat Sheet
===========================

A fast reference guide for building tests using the ArgoBEAST framework.

🔷 Architecture Overview
========================
Feature  →  Steps  →  Actions  →  Pages  →  WebDriver  
What      Describe   Decide      Do        Execute

- **Features** = High-level behaviour descriptions written in Gherkin.
- **Steps** = Logical instructions (Given/When/Then). *Contains branching & decisions.*
- **Actions** = Workflow orchestrators. *Chain Page interactions; no branching.*
- **Pages** = UI element definitions + single UI interactions (“micro-actions”).
- **BasePage** = Provides interaction helpers (click, type, wait…).

📁 Directory Structure
========================
::

   my-tests/
   ├── pages/
   ├── actions/
   ├── features/
   │   └── steps/
   ├── docs/
   │   └── source/
   │       └── beast_docs/  <-- Auto-generated RST lands here
   └── config/
       └── driver.yml

🛠 CLI Quick Commands
========================

.. code-block:: bash

   argobeast init
   argobeast create page <name>
   argobeast create actions <name>
   argobeast create steps <name>
   argobeast create feature <name>
   argobeast generate-docs  <-- NEW!

📚 Living Documentation
========================
Convert Gherkin features into Sphinx-ready RST files.

.. code-block:: bash

   argobeast generate-docs [-y]

- **Source:** Scans ``./features``
- **Target:** Wipes & populates ``./docs/source/beast_docs/``
- **Flag -y:** Skips confirmation (Use for CI/CD pipelines)
- **Warning:** This command is **destructive** to the target folder.

📌 Locators (Pages)
========================
Define at the top of the Page class:

.. code-block:: python

   from selenium.webdriver.common.by import By

   USERNAME = (By.ID, "username")
   SUBMIT   = (By.CSS_SELECTOR, "button.submit")

Best practices:
- Prefer **ID**, **CSS**, **NAME**.
- Avoid long brittle XPATHs.
- Use ALL_CAPS names.

🧩 Page Methods
========================
Pages should expose **single** UI interactions:

.. code-block:: python

   def enter_username(self, value):
       return self.type_text(self.USERNAME, value)

   def click_submit(self):
       return self.click(self.SUBMIT)

❗ Pages should NOT:
- chain workflows  
- contain branching logic  
- decide *why* or *when* something happens  

🎬 Actions
========================
Actions chain page interactions to form workflows:

.. code-block:: python

   class LoginActions(CommonActions):
       PageClass = LoginPage

       def login(self, username, password):
           self.page.enter_username(username)
           self.page.enter_password(password)
           self.page.click_submit()

❗ Actions should NOT:
- contain branching logic  
- interact with WebDriver directly  

🧠 Steps
========================
Steps are where **logic**, **branching**, and **scenario-specific decisions** live.

.. code-block:: python

   @when("I login using {username} and {password}")
   def step_login(context, username, password):
       ctx = BaseStepContext(context)
       actions = ctx.get_actions(LoginActions)
       actions.login(username, password)

❗ Steps SHOULD:
- contain `if…else` logic  
- choose which Actions to run  
- supply test data  

❗ Steps should NOT:
- call WebDriver methods  
- call Page methods directly  
- store business logic inside Actions  

📜 Feature Files
========================
You can add a @skip tag to any scenario to automatically skip a test during a run. This won't count as failure but will show on the report as a skipped scenario. 

Written in Gherkin:

.. code-block:: Gherkin

   Feature: Login
     Scenario: Successful login
       Given I am on the login page
       When I login using correct_user and correct_pass
       Then I should see the home page welcome message

Scenario Outline:

.. code-block:: Gherkin

   Scenario Outline: Login attempts
     Given I am on the login page
     When I login using <username> and <password>
     Then I should see the home page welcome message

     Examples:
       | username   | password     |
       | argobeast  | sup3rs3cr3t! |
       | argoadmin  | password123! |

🎒 BaseStepContext
========================
Your helper for accessing Page + Actions inside steps:

.. code-block:: python

   ctx = BaseStepContext(context)
   page = ctx.get_page(LoginPage)
   actions = ctx.get_actions(LoginActions)

Think of it as a **magic backpack** that gives Steps everything they need.

🚀 CommonActions (helpers)
========================
Includes frequently used patterns like:

- wait_for_text  
- click_element_with_text  
- retry_click  
- scroll_to_bottom  
- wait_for_url_contains  

Documented automatically via:

.. code-block:: rst

   .. automodule:: argo_beast.common_actions.common_actions
      :members:

🧪 Writing Tests — Rule of Thumb
================================

- **Feature** → “What user story are we checking?”
- **Scenario** → “What path are we testing?”
- **Steps** → “Under these conditions, run these workflows.”
- **Actions** → “Perform workflow X using low-level interactions.”
- **Pages** → “Click/type/wait on this specific element.”

🧹 Golden Rules
========================
- Pages = **micro-actions**
- Actions = **linear workflows**
- Steps = **branching & decisions**
- Features = **purely descriptive**

❌ Never call WebDriver directly except inside BasePage  
❌ Never mix Page + Actions logic  
❌ Never put branching logic in Actions  
❌ Never put workflow logic in Pages  

✔️ Always use BaseStepContext inside steps  
✔️ Always name locators clearly  
✔️ Always split steps logically by page