# ArgoBEAST 🚀

![PyPI - Version](https://img.shields.io/pypi/v/argobeast)
![PyPI - License](https://img.shields.io/pypi/l/argobeast)
![Pylint Score](https://img.shields.io/badge/pylint-10.0-brightgreen)

### The Professional Platform-as-a-Product (PaaP) for Web Automation

ArgoBEAST is more than a wrapper; it's a structural engine for high-scale testing. It transforms raw Selenium and Behave into a standardised, professional-grade framework with zero-config scaffolding and a strict separation of concerns.

**Key Architectural Pillars:**
- **Standardized Scaffolding:** Instant generation of the Page Object Model (POM) stack—Pages, Actions, Steps, and Features—via a dedicated CLI.
- **Enterprise-Grade Logic:** Built-in form handling, automatic configuration merging, and high-standard linting (10/10 Pylint).
- **Selenium-First, Mobile-Ready:** Native Selenium support with a roadmap focused on Appium integration for mobile testing.

## Benefits

- 🧱 CLI scaffolding for pages, actions, steps, and project setup

- 🔄 Backend-agnostic architecture (Selenium today, Appium later)

- 🧪 Behave BDD support out of the box

- 📄 Automatic config loading and merging (defaults + user overrides)

- 📦 Packaged and reusable as a .whl

- 🧍 Separation of concerns (Pages → Actions → Steps → Features)

- 💥 Screenshot capture on failure

- 🧰 Extendable actions + reusable BasePage helpers

- 🪄 Magic hooks to enable simple reusable setup and teardown scenarios

- 📝 Easily complete entire website forms with built in form logic

# Installation

Install via pip:
```bash
pip install argobeast
```

Or using UV (recommended for development):
```bash
uv add argobeast
```

To check the installation has run correctly run:

```bash
argobeast hello
```

# Initiating a New Project

To initialise a project run:

```bash
argobeast init
```

This will give you the option to generate example files which can be used as a template for your testing. These starter files will assume you're building tests for a login page.

- actions/login_actions.py
- features/login_feature.feature
- features/steps/login_steps.py
- pages/login_page.py

For more information on how to use these files and create your own tests see [Getting Started](https://pauls-argo.github.io/ArgoBEAST-Documentation/getting_started.html)

Other files generated are:

- requirements.txt (This is a starter file including the initial requirements for your Behave & Selenium testing environment)
- config/driver.yml (This can be customised by the user)
- features/environment.py (Do not touch this file - behave relies on it to run the tests)

### File Structure After Init

```bash
my-tests/
│
├── pages/
│   └── login_page.py
├── actions/
│   └── login_actions.py
├── features/
│   ├── login.feature
│   └── steps/
│       └── login_steps.py
├── config/
│   └── driver.yml
└── features/environment.py   <-- auto-loads framework hooks
```

- Pages
  - Store locators
  - Inherit BasePage
- Actions
  - Contain business logic
  - Inherit CommonActions
- Steps
  - thin Behave glue
  - call Actions
- DriverFactory
  - Selenium setup
- ConfigLoader
  - merges baked defaults with user config

More information on how to use these pages can be found in [Getting Started](https://pauls-argo.github.io/ArgoBEAST-Documentation/getting_started.html)

## Other CLI Commands

ArgoBEAST includes simple commands for generating new pages, actions, steps, and feature files:

```bash
argobeast create page <name of page> # Replace <name of page>
argobeast create steps <name of page>
argobeast create actions <name of page>
argobeast create feature <name of feature> # A page can have multiple features, so make this descriptive
```

### Configure Your Test Target

You can configure your test target by editing config/driver.yml

More information can be found about this in [Getting Started](https://pauls-argo.github.io/ArgoBEAST-Documentation/getting_started.html)


# Roadmap

ArgoBEAST is actively developed with a focus on professional testing environments:

- **Appium Integration:** Expanding the DriverFactory to support mobile automation.
- **Dockerized Execution:** Standardised Dockerfiles for Selenium Grid and headless execution.
- **Reporting Enhancements:** Deep integration for Allure reports (logic currently in `before_all`).