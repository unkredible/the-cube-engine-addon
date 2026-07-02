from dataclasses import dataclass


@dataclass(frozen=True)
class JobResult:
    job_dir: str
    manifest_path: str
    outputs: list[str]
