# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django
from django.conf import settings

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../django_api'))
sys.path.insert(0, os.path.abspath('../django_api/report_schema'))
sys.path.insert(0, os.path.abspath('../django_api/company_schema'))
cwd = os.getcwd()
parent = os.path.dirname(cwd)
sys.path.append(parent)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_api.main_app.settings")


# -- Project information -----------------------------------------------------

project = 'XRBL Scraper'
copyright = '2021, Patrick Donnelly, Brady Snelson, Gilbert Garczynski, ' \
            'Jason Hipkins, Joshua Helperin, ' \
            'Preston Thomson, Siyao Li '
author = 'Patrick Donnelly, Brady Snelson, Gilbert Garczynski, Jason Hipkins, ' \
         'Joshua Helperin, Preston Thomson, ' \
         'Siyao Li '

# The full version, including alpha/beta/rc tags
release = 'V1.0.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinxcontrib_django",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

intersphinx_mapping = {
    'http://docs.python.org/': None,
    'https://docs.djangoproject.com/en/stable': 'https://docs.djangoproject.com/en/stable/_objects',
}
