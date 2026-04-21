<p align="center">
  <img src="https://pauls-argo.github.io/ArgoBEAST-Documentation/_static/logo.png" alt="ArgoBEAST Logo" width="250">
</p>

<h1 align="center">ArgoBEAST 🚀</h1>

<p align="center">
  <img src="https://img.shields.io/pypi/v/argobeast" alt="PyPI - Version">
  <img src="https://img.shields.io/static/v1?label=license&message=Apache%202.0&color=blue" alt="PyPI - License">
  <img src="https://img.shields.io/badge/pylint-10.0-brightgreen" alt="Pylint Score">
</p>

### Stop Building Frameworks. Start Writing Tests.

**ArgoBEAST** is a structural engine for Selenium and Behave. It eliminates the "scramble" of test automation by providing a pre-structured, collaborative ecosystem that forces consistency across your entire team.

**Scaffold a professional Page Object Model (POM) architecture in minutes.**

---

## Why ArgoBEAST?

Most automation projects fail because of inconsistent structure and complex driver logic. ArgoBEAST "crushes" that grunt work by providing the guardrails necessary for collaborative success.

* **⚡ Zero-Config Scaffolding:** Generate a full, professional POM stack—Pages, Actions, Steps, and Features—in seconds via the CLI.
* **🤝 Enforced Collaboration:** Every engineer follows the same pattern: **Pages → Actions → Steps → Features**. No more "lone wolf" code styles.
* **🏗️ Architecture Built-In:** Inherit from `BasePage` and `CommonActions` to get enterprise-grade form handling and element synchronization out of the box.
* **📉 Regression Creep Killer:** Standardized logic makes high-frequency smoke testing easy to implement, maintain, and scale.

---

## Get Started

### 1. Install
```bash
pip install argobeast
# OR (Recommended)
uv add argobeast
```

### 2. Initialize Your Project
```bash
argobeast init
```
This scaffolds a complete, framework-agnostic environment. You can opt-in to generate **example template files** (based on a login scenario) to see the ArgoBEAST pattern in action.

### 3. Build Your First Test
Use the CLI to generate the blueprint for your specific application:
```bash
argobeast create page checkout
argobeast create actions checkout
argobeast create steps checkout
```
Simply add your locators to the `Page` and your business logic to the `Actions`—ArgoBEAST handles the driver injection and configuration merging behind the scenes.

---

## The Workflow: Scalability by Design

ArgoBEAST enforces a clean separation of concerns, ensuring your tests remain readable and maintainable:

| Component | Responsibility | Parent Class |
| :--- | :--- | :--- |
| **Pages** | Store element locators and IDs | `BasePage` |
| **Actions** | High-level business logic & form filling | `CommonActions` |
| **Steps** | Thin Behave "glue" code | N/A |
| **Features** | Human-readable Gherkin scenarios | N/A |

---

## The "No-Logic" Driver Engine

Stop wrestling with `webdriver` initializations and messy `environment.py` hooks. ArgoBEAST abstracts the heavy lifting into a simple configuration layer.

* **⚙️ Logic-Free Configuration:** Control browser types, headless modes, and timeouts via `config/driver.yml`. Change browsers or toggle headless mode without touching a single line of Python code.
* **🪄 Zero-Bloat environment.py:** Framework-level setup/teardown is handled by ArgoBEAST's engine, keeping your project files focused solely on your project logic.
* **📸 Automatic Recovery:** Built-in screenshot capture on every failure, handled internally by framework hooks.
* **📑 Advanced Form Logic:** Use built-in dictionary mapping to complete massive web forms in a single action call.

---

## Roadmap

ArgoBEAST is built for the future of professional QA:
- **V2: Dockerized Execution:** Standardized containers for Selenium Grid and headless execution.
- **V2: Reporting Enhancements:** Native, deep integration for Allure reports.
- **V3: Mobile Support:** Expanding the DriverFactory to support native Appium integration.

---

### Resources
- **Documentation:** [Full Guide & API Reference](https://pauls-argo.github.io/ArgoBEAST-Documentation/)
- **License:** Apache 2.0

**ArgoBEAST: INSTANT VERIFICATION. STRUCTURED, SCALABLE TESTING.**