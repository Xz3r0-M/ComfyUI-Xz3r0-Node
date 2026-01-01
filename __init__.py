"""
Xz3r0 ComfyUI Nodes - A collection of custom nodes
"""

from .Node.Resolution.xsize import Xsize

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "Xsize": Xsize,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Xsize": "Xsize",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]