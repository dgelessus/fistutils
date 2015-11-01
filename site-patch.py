# This is a slightly modified version of setuptools' site-patch.py.
# Because of a minor bug in Pythonista (namely os.environ["PYTHONPATH"]
# containing all sys.path locations) the default site-patch.py fails
# to find the real site.py in the stdlib. This version deletes the
# PYTHONPATH environment variable if this is the case to circumvent this bug.

# Instructions for installing setuptools:
# 1. Copy the distutils folder to your site-packages.
# 2. Install the pydistutils.cfg by following the instructions in that file.
# 3. Download setuptools from https://pypi.python.org/pypi/setuptools/.
#     (Either the zip or tar.gz version works.)
# 4. Unpack it using stash (or some other way).
# 5. Copy the entire contents of this file and paste them into the
#     file at <setuptools-source-folder>/setuptools/site-patch.py.
# 6. Open <setuptools-source-folder>/setup.py.
# 7. Press and hold the "play" icon.
# 8. Type "install" into the text field, and tap Run.
# 9. Once the installation is done, press your home button twice and
#     manually quit Pythonista.
# 10. Restart Pythonista. If there are no errors, you (probably)
#     installed setuptools successfully.

def __boot():
    import sys
    import os
    
    if os.environ.get("PYTHONPATH") == os.pathsep.join(sys.path):
        del os.environ["PYTHONPATH"]
    
    PYTHONPATH = os.environ.get('PYTHONPATH')
    if PYTHONPATH is None or (sys.platform=='win32' and not PYTHONPATH):
        PYTHONPATH = []
    else:
        PYTHONPATH = PYTHONPATH.split(os.pathsep)

    pic = getattr(sys,'path_importer_cache',{})
    stdpath = sys.path[len(PYTHONPATH):]
    mydir = os.path.dirname(__file__)
    #print "searching",stdpath,sys.path

    for item in stdpath:
        if item==mydir or not item:
            continue    # skip if current dir. on Windows, or my own directory
        importer = pic.get(item)
        if importer is not None:
            loader = importer.find_module('site')
            if loader is not None:
                # This should actually reload the current module
                loader.load_module('site')
                break
        else:
            try:
                import imp # Avoid import loop in Python >= 3.3
                stream, path, descr = imp.find_module('site',[item])
            except ImportError:
                continue
            if stream is None:
                continue
            try:
                # This should actually reload the current module
                imp.load_module('site',stream,path,descr)
            finally:
                stream.close()
            break
    else:
        raise ImportError("Couldn't find the real 'site' module")

    #print "loaded", __file__

    known_paths = dict([(makepath(item)[1],1) for item in sys.path]) # 2.2 comp

    oldpos = getattr(sys,'__egginsert',0)   # save old insertion position
    sys.__egginsert = 0                     # and reset the current one

    for item in PYTHONPATH:
        addsitedir(item)

    sys.__egginsert += oldpos           # restore effective old position

    d, nd = makepath(stdpath[0])
    insert_at = None
    new_path = []

    for item in sys.path:
        p, np = makepath(item)

        if np==nd and insert_at is None:
            # We've hit the first 'system' path entry, so added entries go here
            insert_at = len(new_path)

        if np in known_paths or insert_at is None:
            new_path.append(item)
        else:
            # new path after the insert point, back-insert it
            new_path.insert(insert_at, item)
            insert_at += 1

    sys.path[:] = new_path

if __name__=='site':
    __boot()
    del __boot