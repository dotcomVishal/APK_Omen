"use client"

import { useState } from "react"
import { marked } from "marked"

export default function ScanPage() {
  const [file, setFile] = useState<File | null>(null)
  const [report, setReport] = useState("")
  const [scanning, setScanning] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleScan = async () => {
    if (!file) {
      alert("Select APK first")
      return
    }

    setScanning(true)
    setReport("")
    setProgress(0)

    /* Smooth cinematic progress animation */
    let value = 0

    const interval = setInterval(() => {
      value += Math.random() * 10

      if (value >= 92) {
        value = 92
        clearInterval(interval)
      }

      setProgress(Math.floor(value))
    }, 250)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const res = await fetch("http://135.235.195.207:8000/scan", {
        method: "POST",
        body: formData,
      })

      const data = await res.json()

      clearInterval(interval)
      setProgress(100)

      setTimeout(() => {
        setScanning(false)
        setReport(data.report || "No report received")
      }, 400)

    } catch (err) {
      clearInterval(interval)
      setScanning(false)
      alert("Backend died 💀")
    }
  }

  return (
    <main className="scan-page">

      {/* 🌌 Background */}
      <div className="stars"></div>

      {/* 🧠 Main UI */}
      <div className="scan-container">

        <h1 className="scan-title">APK Scan Console</h1>

        <div className="scan-box">

          <input
            className="file-input"
            type="file"
            accept=".apk"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />

          <button
            className="scan-button"
            onClick={handleScan}
            disabled={scanning}
          >
            {scanning ? "Analyzing..." : "Launch Scan"}
          </button>

        </div>

        {/* 📊 Progress */}
        {scanning && (
          <div className="progress-wrapper">
            <div
              className="progress-bar"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}

        {/* 📄 Report */}
        {report && (
          <div
            className="report-box"
            dangerouslySetInnerHTML={{ __html: marked.parse(report) as string }}
          />
        )}

      </div>
    </main>
  )
}
