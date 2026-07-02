import os
import shutil

from .provider_base import AIProviderBase


class LocalMockProvider(AIProviderBase):
    def __init__(self, variants: int = 1):
        self.variants = variants
        self.beauty_path = ""

    def submit_job(self, manifest: dict, files: dict) -> dict:
        self.beauty_path = files["beauty"]
        return {"job_id": manifest["job_id"], "status": "succeeded"}

    def get_status(self, job_id: str) -> dict:
        return {"job_id": job_id, "status": "succeeded"}

    def download_result(self, job_id: str, output_dir: str) -> list[str]:
        outputs = []
        for index in range(1, self.variants + 1):
            output_path = os.path.join(output_dir, f"mock_output_{index:02d}.png")
            shutil.copy2(self.beauty_path, output_path)
            outputs.append(output_path)
        return outputs
