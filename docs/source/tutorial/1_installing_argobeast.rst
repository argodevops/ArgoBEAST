Chapter 1 - Installing ArgoBEAST
================================

1. Prepare your environment (Recommended)
Before installing ArgoBEAST, it is highly recommended to use a virtual environment to manage your dependencies and avoid conflicts with your system Python.

You can use your preferred environment manager (such as venv, conda, or uv). If you are using the standard Python library, you can set one up as follows:

.. code-block:: bash

    # Create a virtual environment
    python -m venv .venv

    # Activate it
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate


2. Install ArgoBEAST
With your environment active, install the latest version directly from our central repository:

.. code-block:: bash

    pip install https://github.com/PaulS-Argo/ArgoBEAST-Documentation/raw/main/latest/argobeast-latest.whl


If you prefer using uv for faster dependency management, you can create an environment and install ArgoBEAST in one go:

.. code-block:: bash

    # Create and activate a virtual environment
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    # Install ArgoBEAST
    uv pip install https://github.com/PaulS-Argo/ArgoBEAST-Documentation/raw/main/latest/argobeast-latest.whl
