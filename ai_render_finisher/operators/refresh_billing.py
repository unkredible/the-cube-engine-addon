import bpy

from ..services.backend_provider import BackendProvider
from ..utils.debug import append_debug


class AIRENDERFINISHER_OT_RefreshBilling(bpy.types.Operator):
    bl_idname = "ai_render_finisher.refresh_billing"
    bl_label = "Refresh Billing"
    bl_description = "Refresh estimated render cost and remaining backend credit"

    def execute(self, context):
        props = context.scene.ai_render_finisher
        addon = context.preferences.addons.get("ai_render_finisher")
        prefs = addon.preferences if addon else None
        if not prefs or prefs.provider != "THECUBE_BACKEND":
            self.report({"WARNING"}, "Billing is available only with The Cube Backend")
            return {"CANCELLED"}

        try:
            provider = BackendProvider(prefs.backend_url, prefs.device_token)
            apply_billing_status(props, provider.billing_status(int(props.variants)))
        except Exception as exc:
            append_debug(props, f"Billing refresh failed: {exc}")
            self.report({"ERROR"}, f"Billing refresh failed: {exc}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Billing refreshed")
        return {"FINISHED"}


def apply_billing_status(props, billing: dict) -> None:
    currency = billing.get("currency") or "USD"
    props.estimated_cost = _money(billing.get("estimated_cost"), currency)
    props.credit_balance = _money(billing.get("current_balance"), currency)
    props.credit_after_estimate = _money(billing.get("remaining_after_estimate"), currency)
    if billing.get("error"):
        append_debug(props, f"Billing error: {billing['error']}")


def _money(value, currency: str) -> str:
    if value is None:
        return "Unknown"
    return f"{float(value):.2f} {currency}"


classes = (AIRENDERFINISHER_OT_RefreshBilling,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
