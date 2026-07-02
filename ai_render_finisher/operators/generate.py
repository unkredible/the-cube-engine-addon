import bpy

from ..jobs.manager import JobManager
from ..utils.debug import append_debug, reset_debug, set_job_state


class AIRENDERFINISHER_OT_Generate(bpy.types.Operator):
    bl_idname = "ai_render_finisher.generate"
    bl_label = "Generate Render"
    bl_description = "Create a render job with The Cube Engine"
    bl_options = {"REGISTER"}

    def execute(self, context):
        props = context.scene.ai_render_finisher
        if props.is_running:
            self.report({"WARNING"}, "The Cube Engine job already running")
            return {"CANCELLED"}
        if props.source == "IMAGE" and not props.source_image:
            self.report({"ERROR"}, "Image source requires an input image")
            return {"CANCELLED"}
        if props.mode != "IMPROVE" and props.style_preset == "CUSTOM_IMAGE" and not props.style_reference_image:
            self.report({"ERROR"}, "Custom Image style requires a style image")
            return {"CANCELLED"}

        props.is_running = True
        reset_debug(props)
        set_job_state(props, "STARTING", "Starting", "Generate pressed", 0.02)
        self._steps = JobManager(context).run_steps()
        self._timer = context.window_manager.event_timer_add(0.15, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "ESC":
            return self._cancel(context)

        if event.type != "TIMER":
            return {"PASS_THROUGH"}

        props = context.scene.ai_render_finisher
        try:
            next(self._steps)
            self._redraw(context)
            return {"RUNNING_MODAL"}
        except StopIteration as stop:
            return self._finish(context, stop.value)
        except Exception as exc:
            set_job_state(props, "ERROR", "Error", str(exc), 1.0)
            self.report({"ERROR"}, f"The Cube Engine failed: {exc}")
            self._cleanup(context)
            return {"CANCELLED"}

    def _finish(self, context, result):
        props = context.scene.ai_render_finisher
        props.last_job_dir = result.job_dir
        props.last_output_path = result.outputs[0] if result.outputs else ""
        append_debug(props, f"Output files: {len(result.outputs)}")
        set_job_state(props, "DONE", "Done", "The Cube Engine job completed", 1.0)
        self.report({"INFO"}, f"The Cube Engine job created: {result.job_dir}")
        self._cleanup(context)
        return {"FINISHED"}

    def _cancel(self, context):
        props = context.scene.ai_render_finisher
        set_job_state(props, "ERROR", "Cancelled", "Job cancelled by user", 1.0)
        self._cleanup(context)
        return {"CANCELLED"}

    def _cleanup(self, context):
        props = context.scene.ai_render_finisher
        props.is_running = False
        if hasattr(self, "_timer"):
            context.window_manager.event_timer_remove(self._timer)
        self._redraw(context)

    def _redraw(self, context):
        for area in context.window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


classes = (AIRENDERFINISHER_OT_Generate,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
