Chapter 8 - Running the Test
############################

If you've followed this tutorial from start to finish you should now have a complete test that:

- Launches the Argo website
- Navigates to the About Us page
- Checks the image of Chris is present

A Note on time.sleep()
**********************

During this tutorial, you might find it helpful to see exactly what the browser is doing at each step. If things are moving too fast for the human eye, you can temporarily import the time module and add a time.sleep(2) between your actions.

This is a great way to "prove" the automation is working and to visually debug your flow.

However, a word of warning: While time.sleep() is a helpful friend during development, it is a sworn enemy of production code.

ArgoBEAST uses Dynamic Waits (which wait only as long as necessary), making your tests fast and stable.

Static Sleeps make tests slow, "flaky," and inefficient.

Feel free to use them to watch the magic happen now, just ensure they are stripped out before you ever consider your code "done."

Running The Test
****************

To run your test simply open a terminal (if you're using a virtual environment ensure it is activated) and run the following command:

.. code-block:: bash
   
   behave

Congratulations! You've just written your first test with ArgoBEAST.