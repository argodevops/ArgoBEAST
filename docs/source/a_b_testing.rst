Configuration-Driven Workflows (A/B Testing)
============================================

A common challenge in modern testing is handling A/B tests, Feature Flags, or "Legacy vs Beta" views where the application flow changes significantly based on the environment.

ArgoBEAST recommends handling this variance at the **Step Definition** layer using a **Router Pattern**.

Instead of cluttering a single Page Object with conditional logic for two completely different UI layouts, you should create distinct Action/Page classes for each version and let the Step Definition decide which one to load.

The Pattern
-----------

1.  **Define the Flag:** Set your feature flag in ``driver.yml``.
2.  **Isolate the Logic:** Create separate Action classes (and Page Objects) for the different versions.
3.  **Route in Python:** Your Step Definition reads the config and requests the appropriate Action class.

Example Implementation
----------------------

**1. driver.yml**

Define which version of the flow you want to test for this run.

.. code-block:: yaml

    # driver.yml
    env: staging
    
    # The toggle
    checkout_flow: "v2_beta"

**2. The Action Classes**

Create a new Action class for the new flow. This ensures your legacy code remains stable while you develop the new version.

* ``features/actions/checkout_legacy.py`` -> ``CheckoutActionsLegacy``
* ``features/actions/checkout_beta.py``   -> ``CheckoutActionsBeta``

**3. The Router Step**

The Gherkin step remains generic ("I perform the checkout"), but the Python implementation acts as a router, leveraging the ArgoBEAST factory to instantiate the correct class.

.. code-block:: python

    from features.actions.checkout_legacy import CheckoutActionsLegacy
    from features.actions.checkout_beta import CheckoutActionsBeta

    @step("I perform the configured checkout sequence")
    def step_impl(context):
        # 1. Get the configuration
        flow_variant = context.beast_config.get("checkout_flow", "legacy")

        # 2. Route to the correct Action Class
        if flow_variant == "v2_beta":
            # ArgoBEAST resolves the Beta Page Object automatically
            actions = context.beast.get_actions(CheckoutActionsBeta)
        else:
            # ArgoBEAST resolves the Legacy Page Object automatically
            actions = context.beast.get_actions(CheckoutActionsLegacy)

        # 3. Execute
        actions.perform_checkout()

**4. The Feature File**

Your feature file remains agnostic to the version. It simply asks for the checkout flow.

.. code-block:: gherkin

    # features/payment.feature
    
    @setup:checkout_flow
    Scenario: Valid Credit Card Payment
      Given I am on the payment screen
      When I perform the configured checkout sequence
      Then I should see the success message

Why this is "The ArgoBEAST Way"
-------------------------------
* **Stability:** You don't risk breaking the legacy flow while scripting the beta flow, as they live in separate files.
* **Clean Stack Traces:** If the beta flow fails, the error points directly to ``CheckoutActionsBeta``, not a generic step file.
* **Zero Technical Debt:** Once the beta becomes the default, you simply delete the `if/else` block and the old `Legacy` class. No complex refactoring required.