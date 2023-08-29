import bpy


class Properties(bpy.types.PropertyGroup):
    type = None

    @classmethod
    def register(cls):
        cls.type.hydra_mrRay = bpy.props.PointerProperty(
            name="Hydra MrRay",
            description="Hydra MrRay properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del cls.type.hydra_mrRay


class RenderProperties(bpy.types.PropertyGroup):
    samplesPerPixel: bpy.props.IntProperty(
        name="Samples Per Pixel",
        description="Amount of samples to take per pixel",
        default=1, min=0
    )


class SceneProperties(Properties):
    type = bpy.types.Scene

    final: bpy.props.PointerProperty(type=RenderProperties)
    viewport: bpy.props.PointerProperty(type=RenderProperties)


register, unregister = bpy.utils.register_classes_factory((
    RenderProperties,
    SceneProperties,
))
