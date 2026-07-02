import os

from ..export.beauty import export_beauty
from ..export.manifest import build_manifest, write_manifest
from ..prompts.builder import build_prompt_pack
from ..services.backend_provider import BackendProvider
from ..services.local_mock_provider import LocalMockProvider
from ..utils.blender_context import show_image_as_render
from ..utils.debug import append_debug, set_job_state
from ..utils.paths import create_job_dir
from ..operators.refresh_billing import apply_billing_status
from .status import JobResult


class JobManager:
    def __init__(self, context):
        self.context = context
        self.scene = context.scene
        self.props = context.scene.ai_render_finisher

    def run(self) -> JobResult:
        steps = self.run_steps()
        while True:
            try:
                next(steps)
            except StopIteration as stop:
                return stop.value

    def run_steps(self):
        set_job_state(self.props, "STARTING", "Starting", "Creating job folder", 0.08)
        yield
        job_dir = create_job_dir(self.scene)
        set_job_state(self.props, "EXPORTING", "Exporting", "Saving beauty.png", 0.20)
        yield
        beauty_path = export_beauty(self.context, job_dir, self.props)
        set_job_state(self.props, "MANIFEST", "Building manifest", "Collecting UI parameters", 0.42)
        yield
        prompt_pack = build_prompt_pack(self.props)

        manifest = build_manifest(
            scene=self.scene,
            props=self.props,
            job_dir=job_dir,
            prompt_pack=prompt_pack,
            passes={"beauty": beauty_path},
        )
        set_job_state(self.props, "MANIFEST", "Writing manifest", "Saving manifest.json", 0.52)
        yield
        manifest_path = write_manifest(manifest, job_dir)

        provider = self._provider()
        set_job_state(self.props, "SUBMITTING", "Submitting", f"Using {provider.__class__.__name__}", 0.65)
        yield
        files = {"beauty": beauty_path}
        style_reference_path = resolve_style_reference_path(self.props, job_dir)
        if style_reference_path:
            files["style_reference"] = style_reference_path
        provider.submit_job(manifest, files)
        set_job_state(self.props, "WAITING", "Waiting", "Waiting provider response", 0.75)
        yield
        provider.get_status(manifest["job_id"])
        for message in getattr(provider, "debug_messages", lambda: [])():
            append_debug(self.props, message)
        if hasattr(provider, "response_billing_status"):
            apply_billing_status(self.props, provider.response_billing_status())
        set_job_state(self.props, "WAITING", "Downloading", "Saving output variants", 0.86)
        yield
        outputs = provider.download_result(manifest["job_id"], job_dir)
        if outputs:
            set_job_state(self.props, "IMPORTING", "Importing", "Opening output as render result", 0.94)
            yield
            show_image_as_render(outputs[0], self.context)

        return JobResult(job_dir=job_dir, manifest_path=manifest_path, outputs=outputs)

    def _provider(self):
        addon = self.context.preferences.addons.get("ai_render_finisher")
        prefs = addon.preferences if addon else None
        if prefs and prefs.provider == "THECUBE_BACKEND":
            return BackendProvider(prefs.backend_url, prefs.device_token)
        return LocalMockProvider(int(self.props.variants))


def bpy_path(path: str) -> str:
    try:
        import bpy

        return bpy.path.abspath(path)
    except Exception:
        return path


def resolve_style_reference_path(props, job_dir: str) -> str:
    if props.mode == "IMPROVE" or props.style_preset != "CUSTOM_IMAGE":
        return ""
    image = props.style_reference_image
    if not image:
        return ""

    path = bpy_path(getattr(image, "filepath", "") or getattr(image, "filepath_raw", ""))
    if path and os.path.exists(path):
        return path

    if getattr(image, "packed_file", None):
        output_path = os.path.join(job_dir, "style_reference.png")
        image.save_render(output_path)
        return output_path

    raise RuntimeError("Custom Image style has no readable image file")
