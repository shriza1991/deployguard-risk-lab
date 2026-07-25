def service_name(environment: str, channel: str) -> str:
    """Build the service label used by health and release support endpoints."""
    return f"deployguard-risk-lab-api ({environment}/{channel})"
