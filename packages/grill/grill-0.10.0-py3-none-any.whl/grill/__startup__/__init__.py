"""This module aims to provide ease startup of The Grill menus and plugins."""
import os
from pathlib import Path


def install(sitedir):
    if "MAYA_PLUG_IN_PATH" in os.environ:
        from . import maya
        maya.install()
    # NOTE: if plugInfo provides more plugins other than USDView, it will need to be
    # executed in deferred evaluation in maya and extended on the houdini package.
    _usd_pluginfo(sitedir)


def _usd_pluginfo(sitedir):
    os.environ["PXR_PLUGINPATH_NAME"] = f"{Path(sitedir) / 'grill' / 'resources' / 'plugInfo.json'}{os.pathsep}{os.environ.get('PXR_PLUGINPATH_NAME', '')}"

