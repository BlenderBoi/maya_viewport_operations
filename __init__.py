bl_info = {
    "name": "Simple Smooth Preview",
    "author": "TinkerBoi",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "description": "Smooth Preview that acts similar like in maya 3",
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
