# fistutils

`distutils` and related libraries patched for use in Pythonista.

These may require the beta version of Pythonsita to work properly, especially `distutils`, because it has to shadow the version from the stdlib. If you're still on Pythonista 1.5, you'll need to modify your `sys.path` manually on every run to make the patched `distutils` take priority over the version from the stdlib.