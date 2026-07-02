from datetime import datetime


MAX_DEBUG_LINES = 12


def reset_debug(props) -> None:
    props.debug_log = ""
    props.status_detail = ""
    props.progress = 0.0
    props.job_stage = "IDLE"


def set_job_state(props, stage: str, status: str, detail: str, progress: float) -> None:
    props.job_stage = stage
    props.status = status
    props.status_detail = detail
    props.progress = progress
    append_debug(props, f"{stage}: {detail}")


def append_debug(props, message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    lines = [line for line in props.debug_log.splitlines() if line]
    lines.append(f"[{timestamp}] {message}")
    props.debug_log = "\n".join(lines[-MAX_DEBUG_LINES:])
