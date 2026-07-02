import base64
import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlencode

from ..constants import ADDON_VERSION_STRING
from .provider_base import AIProviderBase


class BackendProvider(AIProviderBase):
    def __init__(self, backend_url: str, device_token: str = ""):
        self.backend_url = backend_url.rstrip("/")
        self.device_token = device_token
        self.response = None
        self.entitlement = None

    def validate_entitlement(self) -> dict:
        if self.entitlement:
            return self.entitlement
        if not self.device_token:
            raise RuntimeError("Missing addon key. Generate it from the dashboard and paste it in Preferences.")
        payload = self._get_json("/api/addon/entitlement")
        if not payload.get("ok"):
            raise RuntimeError(payload.get("error", "Addon entitlement rejected"))
        self.entitlement = payload.get("entitlement", {})
        return self.entitlement

    def submit_job(self, manifest: dict, files: dict) -> dict:
        self.validate_entitlement()
        encoded_files = {}
        for name, path in files.items():
            encoded_files[name] = {
                "filename": os.path.basename(path),
                "content_type": _content_type(path),
                "base64": _read_b64(path),
            }
        payload = {
            "manifest": manifest,
            "files": encoded_files,
        }
        self.response = self._post_json("/api/render-jobs", payload)
        if not self.response.get("ok"):
            raise RuntimeError(self.response.get("error", "Backend request failed"))
        return {"job_id": self.response["job_id"], "status": "succeeded"}

    def get_status(self, job_id: str) -> dict:
        return {"job_id": job_id, "status": "succeeded"}

    def download_result(self, job_id: str, output_dir: str) -> list[str]:
        if not self.response:
            raise RuntimeError("No backend response available")

        outputs = []
        for index, item in enumerate(self.response.get("outputs", []), start=1):
            filename = item.get("filename") or f"backend_output_{index:02d}.png"
            output_path = os.path.join(output_dir, filename)
            with open(output_path, "wb") as handle:
                handle.write(base64.b64decode(item["base64"]))
            outputs.append(output_path)
        return outputs

    def billing_status(self, variants: int = 1) -> dict:
        query = {"variants": variants}
        return self._get_json(f"/api/billing-status?{urlencode(query)}").get("billing", {})

    def response_billing_status(self) -> dict:
        if not self.response:
            return {}
        return self.response.get("billing", {})

    def debug_messages(self) -> list[str]:
        if not self.response:
            return []
        return [str(message) for message in self.response.get("debug", [])]

    def _post_json(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload).encode("utf-8")
        headers = self._headers()
        headers["Content-Type"] = "application/json"

        request = urllib.request.Request(
            f"{self.backend_url}{path}",
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Backend HTTP {exc.code}: {error_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Backend unreachable: {exc.reason}") from exc

    def _get_json(self, path: str) -> dict:
        headers = self._headers()

        request = urllib.request.Request(f"{self.backend_url}{path}", headers=headers, method="GET")

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Backend HTTP {exc.code}: {error_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Backend unreachable: {exc.reason}") from exc

    def _headers(self) -> dict:
        headers = {
            "X-TheCube-Addon-Version": ADDON_VERSION_STRING,
        }
        if self.device_token:
            headers["Authorization"] = f"Bearer {self.device_token}"
        return headers


def _read_b64(path: str) -> str:
    with open(path, "rb") as handle:
        return base64.b64encode(handle.read()).decode("ascii")


def _content_type(path: str) -> str:
    extension = os.path.splitext(path)[1].lower()
    if extension in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if extension == ".webp":
        return "image/webp"
    return "image/png"
