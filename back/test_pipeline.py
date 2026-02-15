from core.engine import SentinAIEngine
from core.report_adapter import ReportAdapter
from core.ai_report import (
    generate_user_report,
    generate_advanced_report
)

import json

# ------------------------------------------------------------

APK_PATH = "test.apk"   # ← CHANGE IF NEEDED

print("\n==============================")
print(" STARTING APK OMEN PIPELINE ")
print("==============================\n")

# ------------------------------------------------------------
# ENGINE LAYER
# ------------------------------------------------------------

engine = SentinAIEngine(APK_PATH)

raw_findings = engine.start_pipeline()

print("\n--- RAW FINDINGS ---\n")
print(json.dumps(raw_findings, indent=2))

# ------------------------------------------------------------
# NORMALIZATION LAYER
# ------------------------------------------------------------

report = ReportAdapter.normalize(raw_findings)

print("\n--- NORMALIZED REPORT ---\n")
print(json.dumps(report, indent=2))

# ------------------------------------------------------------
# USER REPORT (FILTERED)
# ------------------------------------------------------------

print("\n==============================")
print(" USER SECURITY REPORT ")
print("==============================\n")

user_report = generate_user_report(report)

print(user_report)

# ------------------------------------------------------------
# ADVANCED REPORT (FULL ANALYSIS)
# ------------------------------------------------------------

print("\n==============================")
print(" ADVANCED SECURITY REPORT ")
print("==============================\n")

advanced_report = generate_advanced_report(report)

print(advanced_report)

print("\n==============================")
print(" PIPELINE COMPLETE ")
print("==============================\n")
