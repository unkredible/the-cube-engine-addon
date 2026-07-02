import bpy

from ..constants import ADDON_AUTHOR, ADDON_NAME, ADDON_VERSION_STRING, ADDON_WEBSITE


MODE_CARDS = (
    ("IMPROVE", "Improve", "SHADING_SOLID"),
    ("RESTYLE", "Restyle", "COLOR"),
    ("INVENT", "Invent", "LIGHT"),
)


class AIRENDERFINISHER_PT_MainPanel(bpy.types.Panel):
    bl_label = "The Cube Engine"
    bl_idname = "AIRENDERFINISHER_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "The Cube"

    def draw(self, context):
        layout = self.layout
        props = context.scene.ai_render_finisher
        addon = context.preferences.addons.get("ai_render_finisher")
        prefs = addon.preferences if addon else None

        layout.label(text=f"Build {ADDON_VERSION_STRING}", icon="PLUGIN")
        if prefs and prefs.provider == "THECUBE_BACKEND" and not prefs.device_token:
            warning = layout.box()
            warning.alert = True
            warning.label(text="Addon key missing", icon="ERROR")
            warning.label(text="Generate it from your dashboard and paste it in Preferences.")

        controls = layout.column()
        controls.enabled = not props.is_running
        controls.prop(props, "source")
        if props.source == "IMAGE":
            controls.template_ID_preview(props, "source_image", open="image.open", rows=3, cols=3)
        self._draw_mode_cards(controls, props)
        if props.mode != "IMPROVE":
            controls.prop(props, "style_preset")
            if props.style_preset == "CUSTOM_IMAGE":
                controls.template_ID_preview(props, "style_reference_image", open="image.open", rows=3, cols=3)
        controls.prop(props, "user_prompt")
        controls.prop(props, "variants")
        billing = controls.column(align=True)
        cost_row = billing.row(align=True)
        cost_row.label(text=f"Cost {props.estimated_cost}", icon="INFO")
        cost_row.operator("ai_render_finisher.refresh_billing", text="", icon="FILE_REFRESH")
        billing.label(text=f"Credit {props.credit_balance} -> {props.credit_after_estimate}")
        controls.operator("ai_render_finisher.generate", text="Generate Render", icon="RENDER_STILL")

        status = layout.box()
        status.prop(props, "show_status", text="Debug Status", icon="CONSOLE")
        if props.show_status:
            status.label(text=f"Status: {props.status}")
            status.label(text=f"Stage: {props.job_stage}")
            status.prop(props, "progress", slider=True)
            if props.status_detail:
                status.label(text=props.status_detail)
            if props.last_output_path:
                status.label(text=f"Last Output: {props.last_output_path}")
            status.prop(props, "show_debug")

            if props.show_debug and props.debug_log:
                for line in props.debug_log.splitlines()[-8:]:
                    status.label(text=line)

        about = layout.box()
        about.prop(props, "show_about", text="About Us", icon="INFO")
        if props.show_about:
            about.label(text=ADDON_NAME)
            about.label(text=f"Version {ADDON_VERSION_STRING}")
            about.label(text=ADDON_AUTHOR)
            about.label(text=ADDON_WEBSITE)

    def _draw_mode_cards(self, layout, props):
        layout.label(text="Mode")
        row = layout.row(align=True)
        for mode, title, icon in MODE_CARDS:
            box = row.box()
            column = box.column(align=True)
            column.alignment = "CENTER"
            column.scale_y = 1.8
            button_icon = icon if props.mode != mode else "CHECKMARK"
            op = column.operator("ai_render_finisher.select_mode", text=title, icon=button_icon)
            op.mode = mode


classes = (AIRENDERFINISHER_PT_MainPanel,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
