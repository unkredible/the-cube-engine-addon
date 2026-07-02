import bpy


class AIRENDERFINISHER_Properties(bpy.types.PropertyGroup):
    source: bpy.props.EnumProperty(
        name="Source",
        items=(
            ("VIEWPORT", "Viewport", "Use the current 3D View viewport"),
            ("RENDER", "Render", "Render with Blender settings before AI post-production"),
            ("IMAGE", "Image", "Use a loaded image as the AI input"),
        ),
        default="VIEWPORT",
    )

    source_image: bpy.props.PointerProperty(
        name="Input Image",
        description="Image used as the AI input; its pixel size defines the output resolution",
        type=bpy.types.Image,
    )

    mode: bpy.props.EnumProperty(
        name="Mode",
        items=(
            ("SHAPE_TO_RENDER", "Shape to Render", "Use primitive shapes as positional guide; prompt and style drive the final image"),
            ("GEOMETRY_LOCK", "Geometry Lock", "Preserve geometry over 90% while improving lighting and materials"),
            ("RENDER_FINISH", "Render Finish", "Polish an already good render without inventing new content"),
            ("FREE", "Free", "Let prompt and reference image drive the result"),
        ),
        default="GEOMETRY_LOCK",
    )

    style_preset: bpy.props.EnumProperty(
        name="Style Preset",
        items=(
            ("NONE", "None", "No preset"),
            ("REALISTIC", "Realistic", "Realistic finish"),
            ("AESTHETIC", "Aesthetic", "Aesthetic finish"),
            ("CINEMATIC", "Cinematic", "Cinematic finish"),
            ("TOON", "Toon", "Toon finish"),
            ("LOW_POLY", "Low Poly", "Low-poly finish"),
            ("PIXEL_ART", "Pixel Art", "Pixel-art finish"),
            ("WATERCOLOR", "Watercolor", "Watercolor finish"),
            ("CLAY", "Clay", "Clay render finish"),
            ("CUSTOM_IMAGE", "Custom Image", "Use a loaded image as the style reference"),
        ),
        default="NONE",
    )

    style_reference_image: bpy.props.PointerProperty(
        name="Style Image",
        description="Image used only as visual style reference",
        type=bpy.types.Image,
    )

    user_prompt: bpy.props.StringProperty(
        name="User Prompt",
        description="Creative direction sent to the prompt builder",
        default="",
    )

    ai_strength: bpy.props.FloatProperty(
        name="AI Strength",
        min=0.0,
        max=1.0,
        default=0.55,
        subtype="FACTOR",
    )

    variants: bpy.props.EnumProperty(
        name="Variants",
        items=(("1", "1", "One output"), ("4", "4", "Four outputs"), ("8", "8", "Eight outputs")),
        default="1",
    )

    last_job_dir: bpy.props.StringProperty(
        name="Last Job Folder",
        default="",
        subtype="DIR_PATH",
    )

    last_output_path: bpy.props.StringProperty(
        name="Last Output",
        default="",
        subtype="FILE_PATH",
    )

    estimated_cost: bpy.props.StringProperty(
        name="Estimated Cost",
        default="Unknown",
    )

    credit_balance: bpy.props.StringProperty(
        name="Credit Balance",
        default="Unknown",
    )

    credit_after_estimate: bpy.props.StringProperty(
        name="After This Render",
        default="Unknown",
    )

    is_running: bpy.props.BoolProperty(
        name="Running",
        default=False,
    )

    job_stage: bpy.props.EnumProperty(
        name="Stage",
        items=(
            ("IDLE", "Idle", "No active job"),
            ("STARTING", "Starting", "Preparing job"),
            ("EXPORTING", "Exporting", "Exporting render-control files"),
            ("MANIFEST", "Manifest", "Writing manifest"),
            ("SUBMITTING", "Submitting", "Submitting provider job"),
            ("WAITING", "Waiting", "Waiting for provider response"),
            ("IMPORTING", "Importing", "Importing output"),
            ("DONE", "Done", "Job completed"),
            ("ERROR", "Error", "Job failed"),
        ),
        default="IDLE",
    )

    progress: bpy.props.FloatProperty(
        name="Progress",
        min=0.0,
        max=1.0,
        default=0.0,
        subtype="FACTOR",
    )

    status: bpy.props.StringProperty(
        name="Status",
        default="Idle",
    )

    status_detail: bpy.props.StringProperty(
        name="Detail",
        default="",
    )

    show_status: bpy.props.BoolProperty(
        name="Debug Status",
        default=False,
    )

    show_debug: bpy.props.BoolProperty(
        name="Debug UI",
        default=True,
    )

    show_about: bpy.props.BoolProperty(
        name="About Us",
        default=False,
    )

    debug_log: bpy.props.StringProperty(
        name="Debug Log",
        default="",
    )


classes = (AIRENDERFINISHER_Properties,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ai_render_finisher = bpy.props.PointerProperty(type=AIRENDERFINISHER_Properties)


def unregister():
    del bpy.types.Scene.ai_render_finisher
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
