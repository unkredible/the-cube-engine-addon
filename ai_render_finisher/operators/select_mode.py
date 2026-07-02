import bpy


MODE_AI_STRENGTH = {
    "SHAPE_TO_RENDER": 0.85,
    "GEOMETRY_LOCK": 0.45,
    "RENDER_FINISH": 0.20,
    "FREE": 1.0,
}


class AIRENDERFINISHER_OT_SelectMode(bpy.types.Operator):
    bl_idname = "ai_render_finisher.select_mode"
    bl_label = "Select Mode"
    bl_description = "Select The Cube Engine mode"

    mode: bpy.props.StringProperty()

    def execute(self, context):
        if self.mode not in MODE_AI_STRENGTH:
            return {"CANCELLED"}
        props = context.scene.ai_render_finisher
        props.mode = self.mode
        props.ai_strength = MODE_AI_STRENGTH[self.mode]
        return {"FINISHED"}


classes = (AIRENDERFINISHER_OT_SelectMode,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
