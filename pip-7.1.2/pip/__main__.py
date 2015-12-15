from __future__ import absolute_import

import os
import sys

# Patches for use on Pythonista.

# Reload .pth files, because Pythonista ignores them.
import site
reload(site)

# Need to find a more elegant solution than this.
if any(mod.startswith("pip.") for mod in sys.modules):
    raise Exception("pip is already loaded - please force quit Pythonista to ensure that pip's state is up-to-date.")

"""
# Hard-set the temp directory to "~/Documents/tmp" for testing purposes.
try:
    os.mkdir(os.path.expanduser(u"~/Documents/tmp"))
except OSError as err:
    # Ignore "File exists" errors
    import errno
    if err.errno != errno.EEXIST:
        raise

import tempfile
tempfile.tempdir = os.path.expanduser(u"~/Documents/tmp")
#"""

# End of patches for Pythonista.

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

import pip  # noqa

if __name__ == '__main__':
    sys.exit(pip.main())