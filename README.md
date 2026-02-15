# APK OMEN

**AI-Assisted Static Android Security Engine**

> *"Stop waiting for scans. Start fixing vulnerabilities."*

APK Omen is a stream-based static analysis engine that identifies Android security vulnerabilities through intelligent binary analysis and AI-powered threat assessment.

---

##  Key Features

- ** High-Speed Analysis** - Scans average-sized APKs in under 60 seconds using stream-based extraction
- ** Ghost Permission Detection** - Identifies permissions declared but never used in code
- ** Native Library Analysis** - Scans `.so` (C/C++) libraries for binary protection flaws (PIE/NX)
- ** AI-Powered Intelligence** - Uses Groq API (Llama 3/Mixtral) to explain threat context and impact
- ** OWASP Compliance** - Maps vulnerabilities to OWASP Mobile Top 10 categories
- ** Professional Reports** - Generates boardroom-ready PDF reports automatically

---

##  Team

| Name | Roll Number |
|------|-------------|
| Vishal Singh Rajpurohit | B25339 |
| Dhrudev Popatbhai Sutreja | B25350 |
| Pratyush Rai | B25223 |
| Pratik Sanap | B25222 |

---

##  Quick Links

- ** [Video Walkthrough](INSERT_YOUR_VIDEO_LINK_HERE)**
- ** [Live Dashboard](http://135.235.195.207:3000)**
- ** [GitHub Repository](https://github.com/dotcomVishal/APK_Omen.git)**

---

##  Architecture

APK Omen uses a **stream-based static analysis pipeline** that bypasses traditional decompilation bottlenecks:

### Analysis Pipeline

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│  APK Upload │ ───> │  Extraction  │ ───> │ Risk Mapping│ ───> │  AI Analysis │
│  (Frontend) │      │  (Binary)    │      │  (OWASP)    │      │  (Groq API)  │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
                             │                      │                     │
                             v                      v                     v
                     YARA Rules + DEX         Deterministic          LLM Reasoning
                     Manifest Parsing         Threat Scoring         + Context
```

### How It Works

1. **Ingestion** - User uploads APK via the Next.js frontend
2. **Extraction** - Python backend parses ELF headers, DEX bytecode, and Android Manifest using YARA rules
3. **Risk Mapping** - Raw indicators are deterministically mapped to **OWASP Mobile Top 10** categories
4. **Intelligence Layer** - Structured JSON findings are sent to **Groq API (Llama 3/Mixtral)** for contextual threat analysis
5. **Reporting** - User receives an instant dashboard with threat score and downloadable PDF report

---

##  Installation

### Prerequisites

- **Git** - Version control
- **Python 3.10+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Groq API Key** - Get free tier at [console.groq.com](https://console.groq.com)

### Step 1: Clone the Repository

```bash
git clone https://github.com/dotcomVishal/APK_Omen.git
cd APK_Omen
```

### Step 2: Backend Setup

#### Navigate to backend directory
```bash
cd back
```

#### Create and activate virtual environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Configure AI Integration

1. Open `back/core/ai_report.py`
2. Locate the `api_key` variable
3. Add your Groq API key:

```python
# Inside back/core/ai_report.py
api_key = "gsk_YOUR_ACTUAL_GROQ_KEY_HERE"
```

4. Save the file

#### Start the backend server
```bash
uvicorn main_app:app --reload --port 8000
```

 **Success:** You should see `Uvicorn running on http://127.0.0.1:8000`

### Step 3: Frontend Setup

#### Open a new terminal and navigate to frontend

```bash
cd front
```

#### Install Node packages
```bash
npm install
```

#### Launch the development server
```bash
npm run dev
```

 **Success:** You should see `Ready in X ms` and the app will be available at `http://localhost:3000`

---

##  Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click **"Initialize Scan"**
3. Upload any `.apk` file
4. Watch the real-time analysis:
   - Metadata extraction
   - Threat score calculation
   - AI-powered report generation
5. Download the professional PDF report

---

##  Technology Stack

### Backend
- **FastAPI** - High-performance API framework
- **Python 3.10+** - Core analysis engine
- **YARA** - Pattern matching for threat detection
- **Groq API** - LLM integration (Llama 3/Mixtral)

### Frontend
- **Next.js** - React framework
- **React** - UI library
- **Tailwind CSS** - Styling
- **PDF Generation** - Automated reporting

### Analysis Tools
- DEX bytecode parser
- ELF header analyzer
- Android Manifest parser
- Binary protection scanner

---

##  Features in Detail

### Ghost Permissions
Detects permissions requested in the Android Manifest that are never actually used in the code, helping reduce unnecessary attack surface.

### Native Library Analysis
Scans `.so` (C/C++) libraries for critical binary protection mechanisms:
- PIE (Position Independent Executable)
- NX (No-Execute) bit
- Stack canaries

### AI Context Engine
Goes beyond simple vulnerability detection by providing:
- Contextual threat explanations
- Impact assessment for specific risks
- Remediation recommendations
- Risk prioritization

### OWASP Mobile Top 10 Mapping
Automatically categorizes findings according to industry-standard security frameworks:
- M1: Improper Platform Usage
- M2: Insecure Data Storage
- M3: Insecure Communication
- M4: Insecure Authentication
- M5: Insufficient Cryptography
- M6: Insecure Authorization
- M7: Client Code Quality
- M8: Code Tampering
- M9: Reverse Engineering
- M10: Extraneous Functionality

---

##  Disclaimer

APK Omen is a **defensive security tool** designed for:
- Educational purposes
- Authorized security testing
- Research and development

**The authors are not responsible for any misuse of this software.** Always ensure you have proper authorization before analyzing any application.

---

##  License

This project is developed by Team APK_Omen for educational purposes.

---

##  Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

## 📧 Contact

For questions or collaboration opportunities, please reach out to the team members listed above.

---



**Built with 🔒 by Team APK_Omen**



