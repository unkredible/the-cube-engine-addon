bl_info = {
    "name": "The Cube Engine",
    "author": "Unkredible Studios",
    "version": (0, 1, 33),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > The Cube",
    "description": "AI render post-production for Blender",
    "category": "Render",
}

if "addon_preferences" in locals():
    import importlib

    from . import constants
    from .export import beauty, manifest
    from .jobs import manager, status
    from .prompts import builder
    from .services import backend_provider, local_mock_provider, provider_base
    from .utils import blender_context, debug, paths
    from .operators import refresh_billing, select_mode

    importlib.reload(constants)
    importlib.reload(beauty)
    importlib.reload(manifest)
    importlib.reload(builder)
    importlib.reload(provider_base)
    importlib.reload(local_mock_provider)
    importlib.reload(backend_provider)
    importlib.reload(blender_context)
    importlib.reload(debug)
    importlib.reload(paths)
    importlib.reload(status)
    importlib.reload(manager)
    importlib.reload(addon_preferences)
    importlib.reload(properties)
    importlib.reload(select_mode)
    importlib.reload(refresh_billing)
    importlib.reload(generate)
    importlib.reload(main_panel)
else:
    from . import addon_preferences, properties
    from .operators import generate, refresh_billing, select_mode
    from .panels import main_panel

modules = (
    addon_preferences,
    properties,
    select_mode,
    refresh_billing,
    generate,
    main_panel,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
