import bpy


def show_image_as_render(path: str, context) -> bpy.types.Image:
    image = bpy.data.images.load(path, check_existing=True)
    image.name = "The Cube Result"
    window = getattr(context, "window", None)
    if not window:
        return image

    _open_render_view()
    _assign_to_image_editors(context, image)
    return image


def _open_render_view() -> None:
    if bpy.app.background:
        return
    try:
        bpy.ops.render.view_show("INVOKE_DEFAULT")
    except RuntimeError:
        pass


def _assign_to_image_editors(context, image: bpy.types.Image) -> None:
    window_manager = getattr(context, "window_manager", None)
    current_window = getattr(context, "window", None)
    windows = list(window_manager.windows) if window_manager else []
    if current_window and current_window not in windows:
        windows.append(current_window)

    assigned = False
    for window in windows:
        screen = getattr(window, "screen", None)
        if not screen:
            continue
        for area in screen.areas:
            if area.type == "IMAGE_EDITOR":
                area.spaces.active.image = image
                assigned = True

    if assigned:
        return

    if not current_window:
        return

    for area in current_window.screen.areas:
        if area.type == "IMAGE_EDITOR":
            area.spaces.active.image = image
            return
