"""
Xz3r0 ComfyUI Nodes - A collection of custom nodes
"""

import importlib.util
import os


def is_package_installed(package_name):
    return importlib.util.find_spec(package_name) is not None




# Check for dependencies
missing_deps = []
if not is_package_installed("numpy"):
    missing_deps.append("numpy")
if not is_package_installed("PIL"):
    missing_deps.append("Pillow")

if missing_deps:
    print(f"Xz3r0Nodes: Missing dependencies - {', '.join(missing_deps)}")
    print(f"Please install them using: pip install -r requirements.txt")


from .Node.Resolution.xsize import XSize
from .Node.Image.ximagesave import XImageSave
from .Node.Latent.xloadlatent import XLoadLatent
from .Node.Latent.xsavelatent import XSaveLatent

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "XSize": XSize,
    "XImageSave": XImageSave,
    "XLoadLatent": XLoadLatent,
    "XSaveLatent": XSaveLatent,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "XSize": "XSize",
    "XImageSave": "XImageSave",
    "XLoadLatent": "XLoadLatent",
    "XSaveLatent": "XSaveLatent",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]