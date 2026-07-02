import json
import os

import bpy

from ..constants import ADDON_VERSION_STRING


def build_manifest(scene, props, job_dir: str, prompt_pack: dict, passes: dict) -> dict:
    camera = scene.camera
    resolution = _output_resolution(scene, props)

    return {
        "project": "The Cube Engine",
        "version": ADDON_VERSION_STRING,
        "blender_version": bpy.app.version_string,
        "job_id": os.path.basename(job_dir),
        "source": props.source.lower(),
        "mode": props.mode.lower(),
        "style_preset": props.style_preset.lower() if props.mode != "RENDER_FINISH" else "none",
        "has_style_reference": props.mode != "RENDER_FINISH"
        and props.style_preset == "CUSTOM_IMAGE"
        and bool(props.style_reference_image),
        "user_prompt": props.user_prompt,
        "prompt_strategy": prompt_pack["strategy"],
        "ai_strength": props.ai_strength,
        "preserve_camera": True,
        "variants": int(props.variants),
        "seed": None,
        "resolution": resolution,
        "passes": {name: os.path.basename(path) for name, path in passes.items()},
        "camera": _camera_manifest(camera),
        "provider": {"name": "configured_backend", "model": "server_selected"},
    }


def write_manifest(manifest: dict, job_dir: str) -> str:
    path = os.path.join(job_dir, "manifest.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    return path


def _camera_manifest(camera) -> dict:
    if not camera:
        return {"type": "none", "focal_length_mm": None, "sensor_width_mm": None}

    data = camera.data
    return {
        "type": data.type.lower(),
        "focal_length_mm": data.lens,
        "sensor_width_mm": data.sensor_width,
    }


def _output_resolution(scene, props) -> list[int]:
    if props.source == "IMAGE":
        image = props.source_image
        if not image:
            raise RuntimeError("Input Image source requires an image")
        width, height = image.size
        if width <= 0 or height <= 0:
            raise RuntimeError("Input Image has invalid pixel size")
        return [int(width), int(height)]
    return _render_resolution(scene)


def _render_resolution(scene) -> list[int]:
    scale = scene.render.resolution_percentage / 100.0
    return [
        max(1, int(round(scene.render.resolution_x * scale))),
        max(1, int(round(scene.render.resolution_y * scale))),
    ]
