# fistutils

`distutils`, `setuptools` and `pip` patched for use in Pythonista.

These may require the Pythonista beta version 1.6 or release version 2.0 to work properly, especially `distutils`, because it has to shadow the version from the stdlib. If you're still on Pythonista 1.5, you'll need to modify your `sys.path` manually on every run to make the patched `distutils` take priority over the version from the stdlib.

`pip` technically works, however there are still a number of issues:

1. `pip` MUST NOT BE USED TO UPDATE ITSELF! Otherwise all patches are overwritten and `pip` will no longer work on Pythonista. (The built-in update notification has been disabled in the `pip.conf`.)
2. After any "action" (i. e. installing, upgrading or uninstalling a module) is performed using `pip`, Pythonista must be rebooted. Otherwise `pip`'s "state" (i. e. the database of installed modules and their versions) is not updated properly.
3. Only pure Python modules can be installed. Process forking is disallowed for all iOS apps, which makes invoking an external compiler impossible. Dynamic libraries can also only be loaded if signed by the app developer, meaning that any compiled libraries wouldn't be usable. Oh, and that kind of thing is forbidden by Apple.
4. Modules that come with Pythonista are not recognized. This means that if a module is installed and one of its dependencies is already included in Pythonista, the module will be reinstalled into the user `site-packages` (if it is pure Python) or the installation will fail entirely (if it requires native code).
5. The cache does not work. Currently it is disabled manually through the `pip.conf`, because otherwise a warning about the cache directory's permissions/owner is displayed every time.
6. There may be some odd warnings and strangely formatted output here and there, because the patches to `pip` are *very* hackish. It works, but it's certainly not great.

Any suggestions on how to fix these are welcome. If you have working code, please do submit a pull request.

## Installation

### distutils

1. Move or copy the `distutils` folder into your `site-packages` folder.
2. Open the `pydistutils.cfg` file in the editor.
3. Run this command in the Python prompt to "install" the config file: `import editor, os, shutil; shutil.copyfile(editor.get_path(), os.path.expanduser("~/.pydistutils.cfg"))`

### setuptools

1. Download a source version of `setuptools` (not a wheel) from https://pypi.python.org/pypi/setuptools. (Version 18.3.2 is known to work, future versions should as well, because only a single file is modified.)
2. Extract the downloaded archive using `stash` or another program.
3. Open `site-patch.py` and copy its entire contents, and paste them into `<setuptools-source-folder>/setuptools/site-patch.py`.
4. Open `setuptools`' `setup.py` script.
5. Tap and hold the "play" button, type `install` into the text field, and press Run.
6. Restart Pythonista. Double-press the home button to open the app switcher, swipe the Pythonista "window" up and off the screen, then open Pythonista again.

### pip

1. Open `pip`'s `setup.py` script.
2. Tap and hold the "play" button, type `install` into the text field, and press Run.
3. Open the `pip.conf` file in the editor.
4. Run this command in the Python prompt to "install" the config file: `import editor, os, shutil; os.makedirs(os.path.expanduser("~/.config/pip")); shutil.copyfile(editor.get_path(), os.path.expanduser("~/.config/pip/pip.conf"))`
