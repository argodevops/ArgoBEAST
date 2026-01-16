# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ArgoBEAST'
copyright = '2025, Paul Shears'
author = 'Paul Shears'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.autodoc',
              'sphinx_design']

templates_path = ['_templates']
exclude_patterns = []

html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_static_path = ['_static']
