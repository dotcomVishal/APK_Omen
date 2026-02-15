# APK OMEN
### Next-Gen AI-Assisted Static Android Security Engine

![License](https://img.shields.io/badge/license-MIT-red.svg)
![Status](https://img.shields.io/badge/status-OPERATIONAL-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-LINUX%20%7C%20WIN-lightgrey)

> **"Stop waiting for scans. Start fixing vulnerabilities."**

---

## Team: APK_Omen

| Name | Roll Number | Role |
| :--- | :--- | :--- |
| **Vishal Singh Rajpurohit** | B25339 | Lead Architect & Backend |
| **Dhrudev Popatbhai Sutreja** | B25350 | AI Integration & Research |
| **Pratyush Rai** | B25xxx | Frontend & Visualization |
| **Pratik Sanap** | B25xxx | DevOps & Testing |

---

# PART 1: Project Overview & Demo

### Watch the Demo
[**CLICK HERE TO WATCH THE VIDEO WALKTHROUGH**](INSERT_YOUR_VIDEO_LINK_HERE)

### Live Deployment
[**ACCESS LIVE DASHBOARD**](INSERT_YOUR_DEPLOYED_URL_HERE)

### How It Works
APK Omen is a **Stream-Based Static Analysis Engine**. Unlike traditional tools that rely on slow decompilation or heavy dynamic sandboxing, we extract raw binary features directly from the APK structure to identify threats in seconds.

**The Pipeline:**
1.  **Ingestion:** User uploads APK via the Next.js Frontend.
2.  **Extraction (The Truth):** The Python Backend (`/back`) parses ELF headers, DEX bytecode, and the Android Manifest using YARA rules.
3.  **Risk Mapping (The Logic):** Raw indicators are deterministically mapped to **OWASP Mobile Top 10** categories.
4.  **Intelligence Node (The Reasoning):** We feed the structured JSON findings into the **Groq API (Llama 3/Mixtral)**. The AI generates a human-readable narrative explaining *why* a specific permission or API call is dangerous in this specific context.
5.  **Reporting:** The user gets an instant dashboard with a "Threat Score" and a downloadable, boardroom-ready PDF report.

---

# PART 2: Judges' Guide (Local Installation)

Follow these detailed steps to run the full APK Omen suite on your local machine.

### Prerequisites
* **Git** installed.
* **Python 3.10+** installed.
* **Node.js 18+** installed.
* A **Groq API Key** (Free tier available at [console.groq.com](https://console.groq.com)).

### 1. Clone the Repository
Start by downloading the source code.
```bash
git clone [https://github.com/dotcomVishal/APK_Omen.git](https://github.com/dotcomVishal/APK_Omen.git)
cd APK_Omen
