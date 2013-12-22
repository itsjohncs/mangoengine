import sys
import os

# autodoc needs to be able to find the mangoengine module
sys.path.insert(0, os.path.abspath(".."))

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"MangoEngine"
copyright = u"2013, John Sullivan"

# The short X.Y version.
version = "0.1"

# The full version, including alpha/beta/rc tags.
release = "0.1-rc1"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "nature"
