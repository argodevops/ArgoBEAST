=============
Locators
=============

.. contents::
   :local:
   :depth: 2

❓What Are Locators?
====================
Locators are representations of UI elements. 

They're what the ``Page`` files use to interact with the UI. 

ArgoBEAST makes use of the built in Selenium `By` class to make declaring locators simple. 

They are constructed as a tuple where the first argument is the type and the second is the HTML reference. 

Locator Types
-------------
Selenium makes use of 8 of the most common locator types:

- **CLASS_NAME**
- **CSS_SELECTOR**
- **ID**
- **NAME**
- **XPATH**
- LINK_TEXT
- PARTIAL_LINK_TEXT
- TAG_NAME

In bold are the most commonly used. 

For more information on locators you can, and should, use the Selenium documentation. 
https://www.selenium.dev/documentation/webdriver/elements/locators/

📍 Where to Put Locators
=========================
In ArgoBEAST, locators are scoped globally at the top of your `PageClass` so should be capitalised and spaces separated with an underscore. 

Example:

.. code-block:: python

   from selenium.webdriver.common.by import By

   USER_NAME = (By.ID, "username")
   PASSWORD = (By.ID, "password")

ArgoBEAST keeps locators with the Page they belong to because it makes Pages self-contained and easier to read.

🚧 Best Practices for Maintainable Locators
===========================================
- Be wary of long ``XPATH`` locators. There is a tendency to create unreadable locators based on a raw ``XPATH``. 
This is brittle and could easily break when updates are made to the application. 

- Try to use a unique ``ID`` wherever possible.  

- You should ensure your locators are named appropriately so you can easily reference them. Some common names might be: 

.. code-block:: python

   BURGER_MENU
   USER_NAME
   PASSWORD
