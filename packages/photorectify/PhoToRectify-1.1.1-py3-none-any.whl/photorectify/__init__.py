#!/usr/bin/env python

# Get version from metadata.
try:
    # python >= 3.8
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # python < 3.8
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
