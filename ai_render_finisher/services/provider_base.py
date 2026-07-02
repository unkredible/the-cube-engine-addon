class AIProviderBase:
    def submit_job(self, manifest: dict, files: dict) -> dict:
        raise NotImplementedError

    def get_status(self, job_id: str) -> dict:
        raise NotImplementedError

    def download_result(self, job_id: str, output_dir: str) -> list[str]:
        raise NotImplementedError
