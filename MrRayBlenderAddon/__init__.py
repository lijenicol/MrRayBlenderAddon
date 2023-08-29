bl_info = {
    "name": "Hydra MrRay render engine",
    "author": "Elijah Nicol",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "description": "MrRay render delegate",
    "tracker_url": "",
    "doc_url": "",
    "community": "",
    "downloads": "",
    "main_web": "",
    "support": 'COMMMUNITY',
    "category": "Render"
}


from . import engine, properties, ui


def register():
    engine.register()
    properties.register()
    ui.register()


def unregister():
    ui.unregister()
    properties.unregister()
    engine.unregister()
