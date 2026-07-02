import bpy


class AIRENDERFINISHER_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    provider: bpy.props.EnumProperty(
        name="Provider",
        items=(
            ("LOCAL_MOCK", "Local Mock", "Duplicate the beauty pass locally"),
            ("THECUBE_BACKEND", "The Cube Backend", "Send jobs through the protected backend"),
        ),
        default="LOCAL_MOCK",
    )

    backend_url: bpy.props.StringProperty(
        name="Backend URL",
        default="http://127.0.0.1:8765",
    )

    device_token: bpy.props.StringProperty(
        name="Addon Key",
        description="Unique key generated from your TheCube ENGINE dashboard",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "provider")
        layout.prop(self, "backend_url")
        layout.prop(self, "device_token")
        layout.label(text="Generate this key from the dashboard before using the backend.")


classes = (AIRENDERFINISHER_AddonPreferences,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
