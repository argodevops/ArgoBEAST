Chapter 3 - Configuring the webdriver
=====================================

Before we can write any tests - we must tell ArgoBEAST where the application is that we're testing. This is configured in config/driver.yml

For this tutorial, we're going to be running a test against www.argodevops.co.uk.

You will see that the browser in the config defaults to chrome - ArgoBEAST currently supports:

- Chrome
- Edge
- Firefox

*NOTE*: Selenium autoatically tries to pull the latest webdriver but you will need to have the IE you are using installed on your machine. When using WSL, this can be tricky so you may need to download the drivers manually and point your config using the remote_url option. Further details can be found here.

1. Webdriver config
-------------------

Update your webdriver config as follows. 

.. code-block:: yaml

   browser: chrome
   headless: false
   window_size: "1920,1080"
   remote_url: ""

Note that we've changed headless to false. This tells behave to run a visible browser - this makes troubleshooting your tests much easier as you can watch them run. 

2. Set the base url 
-------------------

Set the base_url to https://www.argodevops.co.uk this tells ArgoBEAST where to navigate to after it creates the driver. 

.. code-block:: yaml

   base_url: "https://www.argodevops.co.uk"

For this tutorial - that's all you need to change. 