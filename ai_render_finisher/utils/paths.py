from datetime import datetime
import os

import bpy


def create_job_dir(scene) -> str:
    base_dir = _project_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    job_dir = os.path.join(base_dir, "ai_render_finisher", "jobs", timestamp)
    os.makedirs(job_dir, exist_ok=True)
    return job_dir


def _project_dir() -> str:
    if bpy.data.filepath:
        return os.path.dirname(bpy.data.filepath)
    return bpy.app.tempdir
