from core.owasp_mapper import map_to_owasp


def build_risk_summary(data):

    manifest = data.get("manifest", {})
    permissions = data.get("permissions", {})
    components = data.get("components", {})
    strings = data.get("strings", {})
    bytecode = data.get("bytecode_references", {})

    observed = []
    risks = []

    # ✅ Debuggable
    if manifest.get("debuggable"):
        observed.append("Application is debuggable")
        risks.append("Attackers may attach debugger and inspect runtime state")

    # ✅ Backup
    if manifest.get("allow_backup") == "true":
        observed.append("ADB backup allowed")
        risks.append("Private app data may be extracted via backup")

    # ✅ Exported components
    exported = components.get("exported_summary", {})
    total_exported = sum(len(v) for v in exported.values())

    if total_exported > 0:
        observed.append(f"{total_exported} exported components detected")
        risks.append("Other apps may interact with exposed entry points")

    # ✅ Suspicious IPs
    if strings.get("ip_addresses"):
        observed.append("Hardcoded IP addresses present")
        risks.append("May indicate fixed external communication endpoints")

    # ✅ Reflection
    if bytecode.get("reflection_usage"):
        observed.append("Reflection usage detected")
        risks.append("May obscure behavior from static analysis")

    owasp = map_to_owasp(observed, risks)

    threat_score = min(len(risks) * 15, 100)

    return {
        "app": data.get("basic_info", {}),
        "observed_risks": observed,
        "potential_impacts": risks,
        "owasp_mapping": owasp,
        "threat_score": threat_score
    }
