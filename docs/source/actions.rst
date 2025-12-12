=============
Actions
=============

.. contents::
   :local:
   :depth: 1

 ❓What Are Actions?
====================
Actions are the glue that holds everything together. An action method will chain together UI Interactions from the Page to complete full tasks. 

Each Action class uses CommonActions which itself uses UI Interactions from the BasePage.

Since these are "Common" actions, they will not cover specific use cases for your application but are handy time-savers and allow you to avoid writing some WebDriver based functionality.  

.. dropdown:: 🌍 Real-world Analogy (Click to expand)

   Imagine a warehouse.

   On the factory floor, there are several workers.
   Each worker can perform a very specific motion:

   stack a box

   label a box

   move a box

   scan a barcode

   They don’t decide when to do these things or why.
   They just do the motion they’ve been trained to do — nothing more.

   Now imagine the floor manager.

   🧑‍💼 The Floor Manager = Actions

   The floor manager stands in the middle of the warehouse holding a clipboard full of instructions.

   He receives a workflow from upper management:

   Build five stacks of boxes

   Label each stack

   Move them to dispatch

   The manager doesn’t question the order, the priority, or whether the job needs to be done today or tomorrow.

   He simply:

   Looks at the workflow he was given

   Breaks it down into small steps

   Sends workers off to perform each step in the correct sequence

   The manager never performs the physical work himself.
   He simply orchestrates the workers in a predictable, repeatable way.

   No decisions.
   No branching.
   No “if admin then…” logic.
   Just run the workflow exactly as defined.

   🧠 And who gives the manager his instructions?

   That would be the CEO.

   🧓 CEO = Steps

   The CEO decides:

   which workflow should run

   when it should run

   under what conditions

   who the workflow applies to

   what data goes into it

   He hands the list of workflows to the floor manager and expects them carried out accurately.

   The CEO never talks directly to the workers and never performs warehouse tasks.
   He stays high-level and outcome-focused.

🎬 Actions Responsibilities
===========================
What it should do
-----------------
- Chain UI Interactions from the Page together to create workflows
- Handle multiple arguments such as username & password
- Linear work-flow only

What it should not do
---------------------  
- Contain any branching logic
- No decisions about when or how the action is called should be included in the actions page

🎨 Creating a New Actions Class
===============================
To initialise a new Actions class, you can use the ArgoBEAST CLI:

``argobeast create actions <name>``

This generates the basic scaffolding for a new Actions class.

The class will assume the existence of the respective PageClass and import it automatically.

*NOTE: If you have not initialised the page, the import will fail*

Example
-------

Below is a simple ActionClass for a login screen. Notice how there is no "if admin...else" logic, just a simple workflow calling the Page UI Interactions. 

.. code-block:: python

   from test_framework.common_actions.common_actions import CommonActions
   from pages.login_page import LoginPage

   class LoginActions(CommonActions):
      PageClass = LoginPage

      def __init__(self, page):
         super().__init__(page)
      
      def log_in(self,username,password):
         self.page.enter_username(username)
         self.page.enter_password(password)
         self.page.click_submit()  

Working With ActionsClass
=========================

Each ActionsClass uses the CommonActions - This is a collection of common UI interaction patterns to save you time repeating logic. 

.. dropdown:: Available Common Actions (Click to Expand)

   .. automodule:: test_framework.common_actions.common_actions
      :members:
      :undoc-members:
      :show-inheritance:

TL;DR
=====

The ActionsClass doesn't contain any complex logic, any decisions and branching happens in the **Steps** 
Actions simply chain together UI Interactions from the respective Page to make something happen. 
