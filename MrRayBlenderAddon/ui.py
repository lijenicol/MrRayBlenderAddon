import bpy

from .engine import MrRayHydraRenderEngine


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {MrRayHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES
    

#
# Quality render settings
#
class MRRAY_HYDRA_RENDER_PT_quality(Panel):
    bl_label = "Quality"

    def draw(self, layout):
        pass


class MRRAY_HYDRA_RENDER_PT_quality_viewport(Panel):
    bl_label = "Viewport"
    bl_parent_id = "MRRAY_HYDRA_RENDER_PT_quality"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        settings = context.scene.hydra_mrRay.viewport
        layout.prop(settings, 'samplesPerPixel')


class MRRAY_HYDRA_RENDER_PT_quality_render(Panel):
    bl_label = "Render"
    bl_parent_id = "MRRAY_HYDRA_RENDER_PT_quality"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        settings = context.scene.hydra_mrRay.final
        layout.prop(settings, 'samplesPerPixel')
    

#
# View layer settings
#
class MRRAY_HYDRA_RENDER_PT_passes(Panel):
    bl_label = "Passes"
    bl_context = "view_layer"

    def draw(self, context):
        pass


class MRRAY_HYDRA_RENDER_PT_passes_data(Panel):
    bl_label = "Data"
    bl_context = "view_layer"
    bl_parent_id = "MRRAY_HYDRA_RENDER_PT_passes"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        view_layer = context.view_layer

        col = layout.column(heading="Include", align=True)
        col.prop(view_layer, "use_pass_combined")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    MRRAY_HYDRA_RENDER_PT_quality,
    MRRAY_HYDRA_RENDER_PT_quality_viewport,
    MRRAY_HYDRA_RENDER_PT_quality_render,
    MRRAY_HYDRA_RENDER_PT_passes,
    MRRAY_HYDRA_RENDER_PT_passes_data,
))


def get_panels():
    # Follow the Cycles model of excluding panels we don't want.
    exclude_panels = {
        'RENDER_PT_stamp',
        'DATA_PT_light',
        'DATA_PT_spot',
        'NODE_DATA_PT_light',
        'DATA_PT_falloff_curve',
        'RENDER_PT_post_processing',
        'RENDER_PT_simplify',
        'SCENE_PT_audio',
        'RENDER_PT_freestyle'
    }
    include_eevee_panels = {
        'MATERIAL_PT_preview',
        'EEVEE_MATERIAL_PT_context_material',
        'EEVEE_MATERIAL_PT_surface',
        'EEVEE_MATERIAL_PT_volume',
        'EEVEE_MATERIAL_PT_settings',
        'EEVEE_WORLD_PT_surface',
    }

    for panel_cls in bpy.types.Panel.__subclasses__():
        if hasattr(panel_cls, 'COMPAT_ENGINES') and (
            ('BLENDER_RENDER' in panel_cls.COMPAT_ENGINES and panel_cls.__name__ not in exclude_panels) or
            ('BLENDER_EEVEE' in panel_cls.COMPAT_ENGINES and panel_cls.__name__ in include_eevee_panels)
        ):
            yield panel_cls


def register():
    register_classes()

    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(MrRayHydraRenderEngine.bl_idname)


def unregister():
    unregister_classes()

    for panel_cls in get_panels():
        if MrRayHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(MrRayHydraRenderEngine.bl_idname)
