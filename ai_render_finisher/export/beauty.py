import os

import bpy


def export_beauty(context, job_dir: str, props) -> str:
    path = os.path.join(job_dir, "beauty.png")

    if props.source == "IMAGE":
        _save_image_datablock(context, props.source_image, path)
        return path

    if props.source == "RENDER":
        _render_camera(context, path)
        return path

    try:
        _render_opengl(context, path, view_context=True)
    except RuntimeError:
        _render_camera(context, path)

    return path


def _save_image_datablock(context, image, path: str) -> None:
    if not image:
        raise RuntimeError("Input Image source requires an image")
    width, height = image.size
    if width <= 0 or height <= 0:
        raise RuntimeError("Input Image has invalid pixel size")

    scene = context.scene
    old_format = scene.render.image_settings.file_format
    try:
        scene.render.image_settings.file_format = "PNG"
        image.save_render(path, scene=scene)
    finally:
        scene.render.image_settings.file_format = old_format


def _render_opengl(context, path: str, view_context: bool) -> None:
    scene = context.scene
    old_filepath = scene.render.filepath
    old_format = scene.render.image_settings.file_format

    try:
        scene.render.filepath = path
        scene.render.image_settings.file_format = "PNG"
        bpy.ops.render.opengl(write_still=True, view_context=view_context)
    finally:
        scene.render.filepath = old_filepath
        scene.render.image_settings.file_format = old_format


def _render_camera(context, path: str) -> None:
    scene = context.scene
    old_filepath = scene.render.filepath
    old_format = scene.render.image_settings.file_format

    try:
        scene.render.filepath = path
        scene.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(write_still=True)
    finally:
        scene.render.filepath = old_filepath
        scene.render.image_settings.file_format = old_format
