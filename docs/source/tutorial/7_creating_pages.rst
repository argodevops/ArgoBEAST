Chapter 7 - Creating Pages
##########################

We are now nearly ready to run our test. The final step is to create the methods that interact with the user interface.

ArgoBEAST follows the principle that page files should contain methods that perform a single, discrete UI interaction. This separation of concerns ensures that each method has a clear, focused responsibility.

When a single page element supports multiple actions, create a dedicated method for each action. For example, if you need to both enter text into a text box and retrieve its current contents, implement two separate methods. This approach allows you to call the appropriate method when needed and keeps your code organised and maintainable.

1. Creating required pages files
********************************

The actions reference 3 pages files:

- ``HomePage``
- ``GeneralPage``
- ``AboutPage``

ArgoBEAST will automatically suffix the page files with ``page``, so you simply need to run the following:

.. code-block:: bash

   argobeast create page Home
   argobeast create page General
   argobeast create page About

2. Breaking down the Page files
*******************************

You should now have 3 page files that look similar to the below:

.. code-block:: python

    from argo_beast.base.base_page import BasePage
    from selenium.webdriver.common.by import By


    class GeneralPage(BasePage):
        def __init__(self, driver, config):
            super().__init__(driver, config)

        # Add your locators here:
        # USERNAME = (By.ID, "username")

Each page is derived from a class called BasePage. This provides a foundation of common user interface interactions—a full breakdown of these actions can be found :ref:here <inline-markup-pages>.

Once the class has been declared, you will see a section within the __init__ method to add your locators. The indentation must match the placeholder code to ensure they are correctly assigned to the page object.

It is possible (and for some, preferable) to extract locators into a separate file, but the ArgoBEAST philosophy is to keep everything relating to a single page in one place for transparency and ease of maintenance.

*Note*: Don't worry about how to find locators for now.

If you're new to testing, think of a locator as the unique "address" or "ID" for an element on the page. It tells the automation tool exactly how to find a specific button or text box within the code, regardless of where it appears on the screen.


3. Setting up the Home Page
***************************

For this tutorial, each page only consists of a single method. On the home page, this will be called `get_home_text()`

- Open the file `pages/home_page.py`
- Add the following locator to the HomePage class:

.. code-block:: python

   TITLE = (By.XPATH, "*//h2[text()='Who We Are']")

Whilst using an XPATH can be brittle, sometimes it is the only way especially when the application under test isn't using unique ids for every element. With the above locator, we're looking for a h2 element where the text exactly matches 'Who We Are'

- Add the following method to the HomePage class:

.. code-block:: python

   def get_home_text(self):
       return self.get_text(self.TITLE)

Notice how we reference the locator using `self`. Any attribute declared at the class level can be accessed anywhere within the class by prefixing it with the `self` argument. 

4. Setting up the General Page
******************************

- open the file `pages/general_page.py`
- Add the following locator to the GeneralPage class.

.. code-block:: python

   NAV_LINKS = (By.CLASS_NAME, "nav-link")

- Add the following method to the GeneralPage class.

.. code-block:: python

    def click_nav_link(self, page):
        nav_links = self.find_all(self.NAV_LINKS)

        for link in nav_links:
            if link.text == page:
                self.click(link)


*A Note on "Internal Logic"*

 - The ArgoBEAST philosophy states that all test logic (decisions, assertions, and flow control) should live in your steps files, while Page Methods should remain responsible for a single UI interaction.
 - You might notice that our click_nav_link method contains a for loop and an if statement. While this looks like logic, it is actually Selection Logic.

*Why this still follows the philosophy:*

 - Single Responsibility: From the perspective of the test, this method does exactly one thing: Clicks a navigation link. The test shouldn't care if that link is found via an ID or by iterating through a list of elements; it just wants the click to happen.

 - Encapsulating the DOM: The "loop and check" is a technical necessity of the UI's structure. By keeping this inside the Page Method, we prevent the steps file from becoming cluttered with the "how" of finding elements.

 - Internal vs. External Logic: * Internal Logic (Page): "How do I find and click the 'About' link in this specific menu?"

 - External Logic (Steps): "If the user is logged in, click 'Profile'; otherwise, click 'Login'."

By keeping the "How" in the Page file and the "What" in the Steps file, we maintain a clean separation of concerns without sacrificing the power of Python.

5. Setting up the About Page
****************************

Our final page is the About page, this is where we're finding Chris and returning `true` if Chris is there, and `false` if Chris is not there. 

- Open the file `pages/about_page.py`
- Replace the entire contents of the file with:

.. code-block:: python

   from argo_beast.base.base_page import BasePage
   from selenium.webdriver.common.by import By


   class AboutPage(BasePage):
       def __init__(self, driver, config):
           super().__init__(driver, config)

       # Add your locators here:
       CHRIS = (By.CSS_SELECTOR, "img[title='Chris']")

       def is_chris_visible(self):
           self.scroll_into_view(self.CHRIS)
           return self.is_visible(self.CHRIS)

Since Selenium interacts directly with the DOM, it can often find and interact with elements even if they aren't currently visible on your screen. This means scroll_into_view(locator) isn't technically required for the test to pass.

However, because we are running in non-headless mode, we've included it so you can actually witness the automation in action. It's a great way to visually confirm that the driver is focusing on the correct part of the page as the test progresses.