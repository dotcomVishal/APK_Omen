from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import tempfile
import os

from core.ai_report import generate_ai_report
from core.risk_engine import build_risk_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXTRACTOR_PATH = "core/extract_new.py"


@app.post("/scan")
async def scan_apk(file: UploadFile = File(...)):

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as tmp:
            tmp.write(await file.read())
            apk_path = tmp.name

        json_output = apk_path + ".json"

        # Run extractor
        subprocess.run(
            ["python3", EXTRACTOR_PATH, apk_path, json_output],
            check=True
        )

        with open(json_output) as f:
            apk_data = json.load(f)

        # Deterministic analysis
        risk_summary = build_risk_summary(apk_data)

        # AI reasoning layer
        ai_report = generate_ai_report(risk_summary)

        return {
            "status": "success",
            "report": risk_summary,
            "ai_report": ai_report
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

    finally:
        if os.path.exists(apk_path):
            os.remove(apk_path)
        if os.path.exists(json_output):
            os.remove(json_output)
