# The Cube Engine

Version: 0.1.37

Blender addon for AI-guided render post-production.

## MVP 0.1

- View3D N-Panel UI.
- Viewport, Render or Image source, four mode cards, style preset, prompt, style reference, billing and variants controls.
- Local job folder creation under `ai_render_finisher/jobs/<timestamp>/`.
- `beauty.png` export through Blender OpenGL render.
- `manifest.json` generation.
- Dashboard-issued addon key required for protected backend calls.
- `LocalMockProvider` output copied as `mock_output_01.png` and additional variants when requested.
- Provider API keys and proprietary prompt logic are intentionally backend-only.

## Install

Zip the `ai_render_finisher` folder and install it in Blender with:

`Edit > Preferences > Add-ons > Install...`
