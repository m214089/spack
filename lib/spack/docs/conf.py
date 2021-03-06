# flake8: noqa
##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
# -*- coding: utf-8 -*-
#
# Spack documentation build configuration file, created by
# sphinx-quickstart on Mon Dec  9 15:32:41 2013.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import re
import shutil
import subprocess
from glob import glob
from sphinx.apidoc import main as sphinx_apidoc

# -- Spack customizations -----------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../external'))
if sys.version_info[0] < 3:
    sys.path.insert(0, os.path.abspath('../external/yaml/lib'))
else:
    sys.path.insert(0, os.path.abspath('../external/yaml/lib3'))
sys.path.append(os.path.abspath('..'))

# Add the Spack bin directory to the path so that we can use its output in docs.
spack_root = '../../..'
os.environ['SPACK_ROOT'] = spack_root
os.environ['PATH'] += '%s%s/bin' % (os.pathsep, spack_root)

# Get the spack version for use in the docs
spack_version =  subprocess.Popen(
    [spack_root + '/bin/spack', '-V'],
    stderr=subprocess.PIPE).communicate()[1].strip().split('.')

# Set an environment variable so that colify will print output like it would to
# a terminal.
os.environ['COLIFY_SIZE'] = '25x120'

#
# Generate package list using spack command
#
with open('package_list.rst', 'w') as plist_file:
    subprocess.Popen(
        [spack_root + '/bin/spack', 'list', '--format=rst'], stdout=plist_file)

#
# Find all the `cmd-spack-*` references and add them to a command index
#
command_names = []
for filename in glob('*rst'):
    with open(filename) as f:
        for line in f:
            match = re.match('.. _(cmd-spack-.*):', line)
            if match:
                command_names.append(match.group(1).strip())

shutil.copy('command_index.in', 'command_index.rst')
with open('command_index.rst', 'a') as index:
    index.write('\n')
    for cmd in sorted(command_names):
        index.write('   * :ref:`%s`\n' % cmd)

#
# Run sphinx-apidoc
#
# Remove any previous API docs
# Read the Docs doesn't clean up after previous builds
# Without this, the API Docs will never actually update
#
apidoc_args = [
    '--force',         # Older versions of Sphinx ignore the first argument
    '--force',         # Overwrite existing files
    '--no-toc',        # Don't create a table of contents file
    '--output-dir=.',  # Directory to place all output
]
sphinx_apidoc(apidoc_args + ['../spack'])
sphinx_apidoc(apidoc_args + ['../llnl'])

#
# Exclude everything in spack.__all__ from indexing.  All of these
# symbols are imported from elsewhere in spack; their inclusion in
# __all__ simply allows package authors to use `from spack import *`.
# Excluding them ensures they're only documented in their "real" module.
#
# This also avoids issues where some of these symbols shadow core spack
# modules.  Sphinx will complain about duplicate docs when this happens.
#
import fileinput, spack
handling_spack = False
for line in fileinput.input('spack.rst', inplace=1):
    if handling_spack:
        if not line.startswith('    :noindex:'):
            print('    :noindex: %s' % ' '.join(spack.__all__))
        handling_spack = False

    if line.startswith('.. automodule::'):
        handling_spack = (line == '.. automodule:: spack\n')

    sys.stdout.write(line)

# Enable todo items
todo_include_todos = True

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.graphviz',
              'sphinx.ext.napoleon',
              'sphinx.ext.todo',
              'sphinxcontrib.programoutput']

# Set default graphviz options
graphviz_dot_args = [
    '-Grankdir=LR', '-Gbgcolor=transparent',
    '-Nshape=box', '-Nfontname=monaco', '-Nfontsize=10']

# Get nice vector graphics
graphviz_output_format = "svg"


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Spack'
copyright = u'2013-2017, Lawrence Livermore National Laboratory.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '.'.join(spack_version[:2])
# The full version, including alpha/beta/rc tags.
release = '.'.join(spack_version[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = { 'logo_only' : True }

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ["_themes"]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '../../../share/spack/logo/spack-logo-white-text-48.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '../../../share/spack/logo/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Spackdoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Spack.tex', u'Spack Documentation',
   u'Todd Gamblin', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'spack', u'Spack Documentation',
     [u'Todd Gamblin'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Spack', u'Spack Documentation',
   u'Todd Gamblin', 'Spack', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'
