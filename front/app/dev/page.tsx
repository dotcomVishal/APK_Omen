"use client";

import { useState, useEffect } from "react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default function DevPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [data, setData] = useState<any>(null);
  const [showRaw, setShowRaw] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      setProgress(0);
      interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return prev;
          const increment = Math.max(1, (90 - prev) / 10);
          return prev + increment;
        });
      }, 200);
    } else {
      setProgress(100);
      setTimeout(() => setProgress(0), 500);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleScan = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setData(null);

    try {
      const res = await fetch("http://localhost:8000/scan", {
        method: "POST",
        body: formData,
      });

      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
      alert("Scan failed. Is the backend running?");
    }

    setLoading(false);
  };

  // --- PDF GENERATION WITH PAGINATION FIX ---
  const downloadPDF = () => {
    if (!data) return;

    const doc = new jsPDF();
    const report = data.report;
    const ai = data.ai_report;

    const colors = {
      primary: [0, 0, 0] as [number, number, number],
      critical: [220, 38, 38] as [number, number, number],
      high: [234, 179, 8] as [number, number, number],
    };

    // Header
    doc.setFont("courier", "bold");
    doc.setFontSize(22);
    doc.setTextColor(colors.primary[0], colors.primary[1], colors.primary[2]);
    doc.text("APK OMEN SECURITY REPORT", 14, 20);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(100, 100, 100);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 26);
    doc.text(`Engine: APK Omen v3.0`, 14, 30);

    doc.setDrawColor(0, 0, 0);
    doc.setLineWidth(0.5);
    doc.line(14, 33, 196, 33);

    let yPos = 45;

    // Score
    const scoreColor = report.threat_score > 70 ? colors.critical : report.threat_score > 40 ? colors.high : [34, 197, 94];
    doc.setFillColor(scoreColor[0], scoreColor[1], scoreColor[2]);
    doc.circle(170, 22, 12, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(10);
    doc.text(`${report.threat_score}`, 166, 24);
    doc.setFontSize(8);
    doc.text("RISK", 166, 28);

    // Metadata Table
    autoTable(doc, {
      startY: yPos,
      head: [['Application Metadata', 'Values']],
      body: [
        ['App Name', report.app?.app_name || 'N/A'],
        ['Package', report.app?.package_name || 'N/A'],
        ['Version', report.app?.version_name || 'N/A'],
        ['SHA256', report.app?.sha256?.substring(0, 32) + '...' || 'N/A'],
      ],
      theme: 'grid',
      headStyles: { fillColor: [0, 0, 0], textColor: 255, font: 'courier' },
      styles: { font: 'courier', fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50 } },
    });

    yPos = (doc as any).lastAutoTable.finalY + 15;

    // --- AI ANALYSIS (FIXED PAGINATION) ---
    doc.setFont("courier", "bold");
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0);
    doc.text("INTELLIGENCE NODE ANALYSIS", 14, yPos);
    yPos += 7;
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(50, 50, 50);

    // Split text into lines
    const splitAi = doc.splitTextToSize(ai || "No AI analysis available.", 180);
    const pageHeight = doc.internal.pageSize.height;
    
    // Loop through lines to check for page breaks
    for (let i = 0; i < splitAi.length; i++) {
        if (yPos > pageHeight - 20) {
            doc.addPage();
            yPos = 20; // Reset to top
        }
        doc.text(splitAi[i], 14, yPos);
        yPos += 5; // Line height
    }
    
    yPos += 10;

    // --- DETAILED TABLES ---
    
    // Secrets Table
    if (report.secrets && report.secrets.length > 0) {
      if (yPos > pageHeight - 40) { doc.addPage(); yPos = 20; }
      
      doc.setFont("courier", "bold");
      doc.setFontSize(12);
      doc.setTextColor(colors.critical[0], colors.critical[1], colors.critical[2]);
      doc.text(`DETECTED SECRETS (${report.secrets.length})`, 14, yPos);
      
      autoTable(doc, {
        startY: yPos + 3,
        head: [['Type', 'Severity', 'Location', 'Snippet']],
        body: report.secrets.map((s: any) => [
          s.type, s.severity, s.location || 'Unknown', s.value?.substring(0, 40)
        ]),
        headStyles: { fillColor: colors.critical, textColor: 255, font: 'courier' },
        styles: { fontSize: 8, font: 'courier', overflow: 'linebreak' },
      });
      yPos = (doc as any).lastAutoTable.finalY + 10;
    }

    // Malware Table
    if (report.malware_indicators && report.malware_indicators.length > 0) {
      if (yPos > pageHeight - 40) { doc.addPage(); yPos = 20; }
      
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(12);
      doc.text(`MALWARE INDICATORS`, 14, yPos);
      
      autoTable(doc, {
        startY: yPos + 3,
        head: [['Indicator', 'Severity', 'Location']],
        body: report.malware_indicators.map((m: any) => [
          m.indicator, m.severity, m.location
        ]),
        headStyles: { fillColor: [0, 0, 0], textColor: 255, font: 'courier' },
        styles: { fontSize: 8, font: 'courier' },
      });
      yPos = (doc as any).lastAutoTable.finalY + 10;
    }

    // Page Numbers
    const pageCount = (doc as any).internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Page ${i} of ${pageCount}`, 100, 290, { align: 'center' });
    }

    doc.save("APKOmen_Report.pdf");
  };

  const downloadRawJSON = () => {
    if (!data?.raw_json) {
        alert("Raw JSON data not found in response.");
        return;
    }
    const blob = new Blob([JSON.stringify(data.raw_json, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "apk_omen_raw.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const getScoreColor = (score: number) => {
    if (score < 40) return "#22c55e"; // Green
    if (score < 70) return "#eab308"; // Yellow
    return "#ef4444"; // Red
  };

  return (
    <div style={styles.scrollContainer}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>APK OMEN</h1>
          <p style={styles.subtitle}>ADVANCED STATIC ANALYSIS ENGINE v3.0</p>
        </div>

        <div style={styles.card}>
          <div style={styles.controls}>
            <input
              type="file"
              accept=".apk"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              style={styles.fileInput}
            />
            <button
              onClick={handleScan}
              disabled={loading || !file}
              style={{
                ...styles.button,
                opacity: loading || !file ? 0.5 : 1,
                cursor: loading || !file ? "not-allowed" : "pointer",
              }}
            >
              {loading ? "SCANNING..." : "INITIALIZE SCAN"}
            </button>
          </div>

          {loading && (
            <div style={styles.progressContainer}>
              <div style={{ ...styles.progressBar, width: `${progress}%` }} />
              <div style={styles.progressText}>{Math.round(progress)}% ANALYZING BINARIES...</div>
            </div>
          )}
        </div>

        {data && (
          <div style={styles.resultsFadeIn}>
            <div style={styles.gridTwo}>
              <div style={styles.card}>
                <h2 style={styles.sectionTitle}>THREAT SCORE</h2>
                <div
                  style={{
                    ...styles.scoreDisplay,
                    color: getScoreColor(data.report?.threat_score || 0),
                    borderColor: getScoreColor(data.report?.threat_score || 0),
                  }}
                >
                  {data.report?.threat_score || 0}
                  <span style={styles.scoreMax}>/ 100</span>
                </div>
              </div>

              <div style={styles.card}>
                <h2 style={styles.sectionTitle}>METADATA</h2>
                <div style={styles.metaList}>
                  <div style={styles.metaItem}>
                    <span style={styles.metaLabel}>APP NAME:</span>
                    <span>{data.report?.app?.app_name || "N/A"}</span>
                  </div>
                  <div style={styles.metaItem}>
                    <span style={styles.metaLabel}>PACKAGE:</span>
                    <span>{data.report?.app?.package_name || "N/A"}</span>
                  </div>
                  <div style={styles.metaItem}>
                    <span style={styles.metaLabel}>VERSION:</span>
                    <span>{data.report?.app?.version_name || "1.0"}</span>
                  </div>
                   <div style={styles.metaItem}>
                    <span style={styles.metaLabel}>SHA256:</span>
                    <span style={styles.hashText}>{data.report?.app?.sha256?.substring(0, 16)}...</span>
                  </div>
                </div>
              </div>
            </div>

            <div style={styles.card}>
              <h2 style={styles.sectionTitle}>INTELLIGENCE NODE LOG</h2>
              <div style={styles.aiReportContent}>
                {data.ai_report || "Intelligence Node analysis pending..."}
              </div>
            </div>

            <div style={styles.gridTwo}>
              <div style={styles.card}>
                <h2 style={styles.sectionTitle}>OBSERVED RISKS</h2>
                <ul style={styles.riskList}>
                  {data.report?.observed_risks?.map((r: string, i: number) => (
                    <li key={i} style={styles.riskItem}>• {r}</li>
                  )) || <li>No observed risks listed.</li>}
                </ul>
              </div>

              <div style={styles.card}>
                <h2 style={styles.sectionTitle}>POTENTIAL IMPACTS</h2>
                <ul style={styles.riskList}>
                  {data.report?.potential_impacts?.map((r: string, i: number) => (
                    <li key={i} style={styles.riskItem}>• {r}</li>
                  )) || <li>No potential impacts listed.</li>}
                </ul>
              </div>
            </div>

             <div style={styles.card}>
                <h2 style={styles.sectionTitle}>OWASP MAPPING</h2>
                <div style={styles.tagContainer}>
                  {data.report?.owasp_mapping?.map((r: string, i: number) => (
                    <span key={i} style={styles.tag}>{r}</span>
                  )) || <span style={styles.tag}>None</span>}
                </div>
            </div>

            <div style={styles.actionRow}>
              <button onClick={downloadPDF} style={styles.secondaryButton}>
                DOWNLOAD PDF REPORT
              </button>
              <button onClick={downloadRawJSON} style={styles.secondaryButton}>
                DOWNLOAD RAW JSON
              </button>
              <button
                onClick={() => setShowRaw(!showRaw)}
                style={styles.secondaryButton}
              >
                {showRaw ? "HIDE RAW DATA" : "VIEW RAW DATA"}
              </button>
            </div>

            {showRaw && (
              <div style={styles.rawContainer}>
                <pre style={styles.preBlock}>
                  {data.raw_json 
                    ? JSON.stringify(data.raw_json, null, 2) 
                    : "Error: 'raw_json' field is missing from response."}
                </pre>
              </div>
            )}
            
            <div style={{ height: "100px" }}></div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  scrollContainer: {
    position: "fixed",
    top: 0, left: 0, right: 0, bottom: 0,
    width: "100vw", height: "100vh",
    overflowY: "auto", overflowX: "hidden",
    backgroundColor: "#000000", color: "#e5e5e5",
    fontFamily: "'Courier New', Courier, monospace",
    padding: "40px 20px 100px 20px",
    boxSizing: "border-box", zIndex: 9999,
  },
  container: {
    maxWidth: "1000px", margin: "0 auto",
    display: "flex", flexDirection: "column",
    gap: "24px", paddingBottom: "100px",
  },
  header: { textAlign: "center", marginBottom: "20px" },
  title: {
    fontSize: "2.5rem", fontWeight: "700", letterSpacing: "2px",
    margin: "0 0 5px 0", color: "#ffffff", textTransform: "uppercase",
  },
  subtitle: { color: "#666", fontSize: "0.9rem", letterSpacing: "1px" },
  card: { backgroundColor: "#050505", border: "1px solid #333", padding: "24px" },
  controls: { display: "flex", gap: "16px", flexWrap: "wrap", justifyContent: "center" },
  fileInput: {
    padding: "12px", backgroundColor: "#000", border: "1px solid #444",
    color: "#fff", cursor: "pointer", width: "100%", maxWidth: "300px",
  },
  button: {
    backgroundColor: "#fff", color: "#000", border: "1px solid #fff",
    padding: "12px 24px", fontWeight: "bold", fontSize: "1rem", cursor: "pointer",
  },
  progressContainer: {
    marginTop: "20px", width: "100%", backgroundColor: "#111",
    height: "20px", border: "1px solid #333", position: "relative",
  },
  progressBar: { height: "100%", backgroundColor: "#fff", transition: "width 0.2s" },
  progressText: {
    position: "absolute", top: "0", left: "0", width: "100%", height: "100%",
    display: "flex", alignItems: "center", justifyContent: "center",
    color: "#000", fontSize: "0.8rem", fontWeight: "bold", mixBlendMode: "difference",
  },
  gridTwo: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))", gap: "24px" },
  sectionTitle: {
    fontSize: "1rem", fontWeight: "700", color: "#666", marginTop: 0,
    marginBottom: "16px", borderBottom: "1px solid #333", paddingBottom: "8px",
  },
  scoreDisplay: {
    fontSize: "3.5rem", fontWeight: "800", textAlign: "center", padding: "20px",
    border: "4px solid", borderRadius: "50%", width: "120px", height: "120px",
    display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
    margin: "0 auto", lineHeight: "1", backgroundColor: "#000",
  },
  scoreMax: { fontSize: "0.9rem", color: "#666", marginTop: "5px" },
  metaList: { display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.9rem" },
  metaItem: { display: "flex", justifyContent: "space-between", borderBottom: "1px solid #222", paddingBottom: "8px" },
  metaLabel: { color: "#888" },
  hashText: { fontFamily: "monospace", color: "#444" },
  aiReportContent: {
    whiteSpace: "pre-wrap", wordWrap: "break-word", lineHeight: "1.6", color: "#ccc",
    fontSize: "0.9rem", backgroundColor: "#0a0a0a", padding: "15px", borderLeft: "2px solid #fff",
  },
  riskList: { paddingLeft: "0", listStyle: "none", margin: 0, color: "#ccc", fontSize: "0.9rem" },
  riskItem: { marginBottom: "10px", lineHeight: "1.4" },
  tagContainer: { display: "flex", flexWrap: "wrap", gap: "8px" },
  tag: { backgroundColor: "#111", color: "#ccc", padding: "4px 10px", fontSize: "0.8rem", border: "1px solid #333" },
  actionRow: { display: "flex", justifyContent: "center", gap: "12px", marginTop: "10px", flexWrap: "wrap", paddingBottom: "20px" },
  secondaryButton: {
    backgroundColor: "#000", border: "1px solid #444", color: "#fff",
    padding: "10px 20px", cursor: "pointer", fontSize: "0.8rem", textTransform: "uppercase",
  },
  rawContainer: { backgroundColor: "#000", padding: "20px", border: "1px solid #333", overflowX: "auto" },
  preBlock: { fontFamily: "monospace", fontSize: "0.8rem", color: "#0f0", margin: 0 },
  resultsFadeIn: { display: "flex", flexDirection: "column", gap: "24px", animation: "fadeIn 0.5s ease-in" },
};
