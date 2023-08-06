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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'tulips'
copyright = '2021, Eva Laplace'
author = 'Eva Laplace'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_rtd_theme', 'nbsphinx', 'sphinx.ext.mathjax', 'sphinx_copybutton','sphinx_gallery.load_style']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ['energy_and_mixing_diagram.ipynb']

# Trying to create thumbnail, doesnt work yet
nbsphinx_thumbnails = {
    'perceived_color_diagram': 'figures/thumb1.png',
    'energy_and_mixing_diagram': 'figures/thumb2.png',
}

# Add a heading to notebooks
nbsphinx_prolog = """
{% set docname = env.doc2path(env.docname, base=None) %}
.. note:: This tutorial was generated from a Jupyter notebook that can be
          downloaded `here <https://bitbucket.org/elaplace/tulips/src/master/docs/source/{{ docname }}>`_.
.. raw:: html
    <style>
        .nbinput .prompt,
        .nboutput .prompt {
            display: none;
        }
    </style>
"""



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_favicon = 'figures/tulips_icon.ico'
html_logo = "figures/tulips_logo.png"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

nbsphinx_allow_errors = True