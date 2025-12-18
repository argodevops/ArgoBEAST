## ArgoBEAST

### BEhave And Selenium Testing Framework

A Python-based test automation framework for web applications, built on Behave, Selenium, and a clean Page Object Model. Includes a CLI tool for scaffolding pages, actions, steps, and project structure.

## Benefits

- 🧱 CLI scaffolding for pages, actions, steps, and project setup

- 🔄 Backend-agnostic architecture (Selenium today, Playwright optional later)

- 🧪 Behave BDD support out of the box

- 📄 Automatic config loading and merging (defaults + user overrides)

- 📦 Packaged and reusable as a .whl

- 🧍 Separation of concerns (Pages → Actions → Steps → Features)

- 💥 Screenshot capture on failure

- 🧰 Extendable actions + reusable BasePage helpers

# Build & Installation

To build the whl you will need to ensure you have `build` installed and then build the whl.

```bash
pip install build
python3 -m build # Run this from the root directory
```

The whl will output to the dist folder. From here you can download/copy to any other location.
To install run:

```bash
pip install argobeast-x.x.x-py3-none-any.whl
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

For more information on how to use these files and create your own tests see [Getting Started](docs/source/getting_started.rst)

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

More information on how to use these pages can be found in [Getting Started](docs/source/getting_started.rst)

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

More information can be found about this in [Getting Started](docs/source/getting_started.rst)

# Project Directory Tree

```
.
├── MANIFEST.in
├── README.md
├── docs
│   └── source
│       ├── _static
│       │   └── logo.png
│       ├── a_b_testing.rst
│       ├── actions.rst
│       ├── advanced_features.rst
│       ├── allure_reporting.rst
│       ├── cheat_sheet.rst
│       ├── conf.py
│       ├── configuration_guide.rst
│       ├── features.rst
│       ├── form_population_engine.rst
│       ├── getting_started.rst
│       ├── global_config.rst
│       ├── index.rst
│       ├── locators.rst
│       ├── magic_hooks.rst
│       ├── pages.rst
│       └── steps.rst
├── pyproject.toml
├── requirements_dev.txt
├── src
│   └── argo_beast
│       ├── base
│       │   ├── base_page.py
│       │   ├── base_step_context.py
│       │   └── driver_factory.py
│       ├── behave_integration
│       │   ├── behave_helpers.py
│       │   ├── environment.py
│       │   └── report_manager.py
│       ├── cli
│       │   ├── create.py
│       │   ├── helpers.py
│       │   ├── main.py
│       │   └── templates.py
│       ├── common_actions
│       │   └── common_actions.py
│       └── config
│           ├── defaults.yml
│           └── loader.py
└── tests
```

# Roadmap

ArgoBEAST is still under development. Below is the current roadmap.

- Extend for Appium support

- Docker integration

- Dockerfiles for running with no browser (Selenium Grid - already included)
