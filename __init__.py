bl_info = {
    "name": "Maya Viewport Operations",
    "author": "TinkerBoi",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "description": "Maya Viewport Operations",
    "wiki_url": "",
    "category": "Utility",
}


import bpy
from . import Operator
from . import Preferences


def register():

    Operator.register()
    Preferences.register()


def unregister():

    Operator.unregister()
    Preferences.unregister()


if __name__ == "__main__":
    register()
