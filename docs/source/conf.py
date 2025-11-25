# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ArgoBEAST'
copyright = '2025, Paul S'
author = 'Paul S'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.autodoc', "sphinx_design"]

templates_path = ['_templates']
exclude_patterns = []
mermaid_output_format = "svg"
mermaid_version = "10.6.0"
# mermaid_cmd = 'mmdc'
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_static_path = ['_static']
