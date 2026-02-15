# APK OMEN
### AI-Assisted Static Android Security Engine


> **"Stop waiting for scans. Start fixing vulnerabilities."**

---

## Team: APK_Omen

| Name | Roll Number | 
| :--- | :--- | :--- |
| **Vishal Singh Rajpurohit** | B25339 | 
| **Dhrudev Popatbhai Sutreja** | B25350 | 
| **Pratyush Rai** | B25223 | 
| **Pratik Sanap** | B25222 | 

---

# PART 1: Project Overview & Demo

### Watch the Demo
[**CLICK HERE TO WATCH THE VIDEO WALKTHROUGH**](INSERT_YOUR_VIDEO_LINK_HERE)

### Live Deployment
[**ACCESS LIVE DASHBOARD**](http://135.235.195.207:3000)

### How It Works
APK Omen is a **Stream-Based Static Analysis Engine**. Unlike traditional tools that rely on slow decompilation or heavy dynamic sandboxing, we extract raw binary features directly from the APK structure to identify threats.

**The Pipeline:**
1.  **Ingestion:** User uploads APK via the Next.js Frontend.
2.  **Extraction (The Truth):** The Python Backend (`/back`) parses ELF headers, DEX bytecode, and the Android Manifest using YARA rules.
3.  **Risk Mapping (The Logic):** Raw indicators are deterministically mapped to **OWASP Mobile Top 10** categories.
4.  **Intelligence Node (The Reasoning):** We feed the structured JSON findings into the **Groq API (Llama 3/Mixtral)**. The AI generates a human-readable narrative explaining *why* a specific permission or API call is dangerous in this specific context.
5.  **Reporting:** The user gets an instant dashboard with a "Threat Score" and a downloadable, boardroom-ready PDF report.

---

# PART 2: Guide (Local Installation)

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
2. Setup the "Brain" (Backend)
The backend is built with FastAPI. It handles the heavy lifting: file parsing, static analysis, and AI communication.

Step A: Navigate to the backend folder

Bash
cd back
Step B: Create a virtual environment
This keeps dependencies isolated.

Windows:

Bash
python -m venv venv
.\venv\Scripts\activate
Mac/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Step C: Install dependencies

Bash
pip install -r requirements.txt
Step D: Configure the Intelligence Node (AI Key)
Crucial Step: The AI reporting feature requires a Groq API key.

Open the file back/core/ai_report.py.

Locate the line where api_key is defined (it is currently commented out or empty).

Uncomment it and paste your key inside the quotes like this:

Python
# Inside back/core/ai_report.py
api_key = "gsk_YOUR_ACTUAL_GROQ_KEY_HERE"
Save the file.

Step E: Ignite the Engine
Start the backend server.

Bash
uvicorn main_app:app --reload --port 8000
 Success: You should see "Uvicorn running on https://www.google.com/search?q=http://127.0.0.1:8000". Keep this terminal open!

3. Setup the "Face" (Frontend)
The frontend is built with Next.js. It provides the dark-mode terminal interface and PDF generation.

Step A: Open a New Terminal
Do not close the backend terminal. Open a new window and navigate to the project root.

Step B: Navigate to the frontend folder

Bash
cd ../front
Step C: Install Node packages

Bash
npm install
Step D: Launch the UI

Bash
npm run dev
 Success: You should see "Ready in xxxxms".

4. Run the Analysis
Open your browser and go to http://localhost:3000.

Click "Initialize Scan".

Upload any .apk file.

Watch as the engine extracts metadata, calculates the threat score, and generates the AI report in real-time.

Key Features for Evaluation
Speed: Scans average-sized APKs in under 60 seconds using stream-based extraction.

Ghost Permissions: Detects permissions requested in the Manifest that are never used in the actual code (reducing attack surface).

Native Analysis: Scans .so (C/C++) libraries for binary protection flaws like missing PIE/NX.

AI Context: Doesn't just say "Risk Found"—it explains the impact of that risk using LLM reasoning.

Professional Reports: Generates vector-quality PDF reports automatically.

Disclaimer
APK Omen is a defensive security tool designed for educational and authorized testing purposes only. The authors are not responsible for any misuse of this software.

Built by Team APK_Omen
