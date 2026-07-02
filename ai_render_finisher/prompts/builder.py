def build_prompt_pack(props) -> dict:
    return {
        "strategy": {
            "mode": props.mode.lower(),
            "style_preset": props.style_preset.lower() if props.mode != "IMPROVE" else "none",
            "has_style_reference": props.mode != "IMPROVE"
            and props.style_preset == "CUSTOM_IMAGE"
            and bool(props.style_reference_image),
            "has_user_prompt": bool(props.user_prompt.strip()),
            "ai_strength": props.ai_strength,
        }
    }
