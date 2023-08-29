import bpy


class MrRayHydraRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = 'HYDRA_MRRAY'
    bl_label = "Hydra MrRay"
    bl_info = "MrRay render delegate"

    bl_use_preview = True
    bl_use_gpu_context = False

    bl_delegate_id = 'HdMrRayRendererPlugin'

    def get_render_settings(self, engine_type):
        settings = bpy.context.scene.hydra_mrRay.viewport if engine_type == 'VIEWPORT' else \
            bpy.context.scene.hydra_mrRay.final
        return {
            'convergedSamplesPerPixel': settings.samplesPerPixel,
            'aovToken:Combined': "color",
        }

    def update_render_passes(self, scene, render_layer):
        if render_layer.use_pass_combined:
            self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')


register, unregister = bpy.utils.register_classes_factory((
    MrRayHydraRenderEngine,
))
