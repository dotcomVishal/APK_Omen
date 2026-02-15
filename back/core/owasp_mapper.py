OWASP_MAP = {
    "debuggable": "M7: Client Code Quality",
    "backup": "M2: Insecure Data Storage",
    "exported": "M1: Improper Platform Usage",
    "ip": "M3: Insecure Communication",
    "reflection": "M8: Code Tampering"
}


def map_to_owasp(observed, risks):

    mappings = set()

    for item in observed:

        lower = item.lower()

        if "debuggable" in lower:
            mappings.add(OWASP_MAP["debuggable"])

        if "backup" in lower:
            mappings.add(OWASP_MAP["backup"])

        if "exported" in lower:
            mappings.add(OWASP_MAP["exported"])

        if "ip" in lower:
            mappings.add(OWASP_MAP["ip"])

        if "reflection" in lower:
            mappings.add(OWASP_MAP["reflection"])

    return list(mappings)
