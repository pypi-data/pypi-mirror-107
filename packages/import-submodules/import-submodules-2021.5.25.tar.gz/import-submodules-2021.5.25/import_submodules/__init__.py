import importlib
import inspect
import os
import pkgutil
import sys

def getmodule(path):
    for name,module in sys.modules.items():
        if hasattr(module,'__file__') and module.__file__==path:
            return module

def import_submodules():
    for frame in inspect.getouterframes(inspect.currentframe()):
        if frame.filename and os.path.exists(frame.filename) and frame.filename!=__file__:
            parent_module = getmodule(frame.filename)
            dirname = os.path.dirname(frame.filename)
            __path__ = pkgutil.extend_path([dirname], __name__)
            for imp, name, ispackage in pkgutil.walk_packages(path=[dirname], prefix=parent_module.__name__+'.'):
                importlib.import_module(name)
            return

def import_all_from_submodules():
    for frame in inspect.getouterframes(inspect.currentframe()):
        if frame.filename and os.path.exists(frame.filename) and frame.filename!=__file__:
            parent_module = getmodule(frame.filename)
            dirname = os.path.dirname(frame.filename)
            __path__ = pkgutil.extend_path([dirname], __name__)
            for imp, name, ispackage in pkgutil.walk_packages(path=[dirname], prefix=parent_module.__name__+'.'):
                module = importlib.import_module(name)
                for k in getattr(module,'__all__',list(module.__dict__.keys())):
                    setattr(parent_module,k,getattr(module,k))
            return


