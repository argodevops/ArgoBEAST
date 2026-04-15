Chapter 6 - Creating Actions
############################

In the previous chapter, we created steps. The steps call actions but currently, there are no actions to be called so let's get into it.

1. Creating required actions files
**********************************

The steps reference 3 actions files:

- ``HomeActions``
- ``GeneralActions``
- ``AboutActions``

ArgoBEAST will automatically suffix the actions files with ``Actions``, so you simply need to run the following:

.. code-block:: bash

   argobeast create actions Home
   argobeast create actions General
   argobeast create actions About

You'll notice the code within each file is very limited. Furthermore, you'll notice they each reference page files that don't exist yet:

.. code-block:: python

   from pages.general_page import GeneralPage

As with the steps, don't panic! This tutorial is designed to create the files from the bottom up to help you understand the flow of the POM.

2. Home Action
**************

Our first action is `get_home_text()` create this as below. 

1. Open the file `actions/home_actions.py`
2. Replace the entire contents of the file with:

.. code-block:: python

   from argo_beast.common_actions.common_actions import CommonActions
   from pages.home_page import HomePage


   class HomeActions(CommonActions):
       PageClass = HomePage

       def __init__(self, page):
            super().__init__(page)

       def get_home_text(self):
           return self.page.get_home_text()

Note that we return the result here. While returning values is not typically necessary for `given` actions, in this tutorial we need to return the result so we can assert that it matches our expected value. 


3. General Action
*****************

Next we need to write the code for `navigate_to_page(page)` this is a general action as it can be reused later to navigate to other parts of the website. 

We're also passing in the `page` argument - this will indicate which page we would like to visit. 

1. Open the file `actions/general_actions.py`
2. Replace the entire contents of the file with:

.. code-block:: python


    from argo_beast.common_actions.common_actions import CommonActions
    from pages.general_page import GeneralPage


    class GeneralActions(CommonActions):
        PageClass = GeneralPage

        def __init__(self, page):
            super().__init__(page)

        def navigate_to_page(self, page):
            self.page.click_nav_link(page)

4. About Action
***************

Lastly, we need to create the action that relates to our `then` step `is_chris_visible()`. 

Since Chris "Lives" on the About Us page - We'll be creating this as an `About` Action. 

We're looking for this image. 

.. image:: /_static/chris.png
    :alt: Chris profile from argodevops.co.uk

1. Open the file `actions/about_actions.py`
2. Replace the entire contents of the file with:

.. code-block:: python

    from argo_beast.common_actions.common_actions import CommonActions
    from pages.about_page import AboutPage


    class AboutActions(CommonActions):
        PageClass = AboutPage

        def __init__(self, page):
            super().__init__(page)

        def is_chris_visible(self):
            return self.page.is_chris_visible()

As with our `given` step, we're returning the result. This is extremely important for a `then` step as it allows us to assert the result of the test. 
