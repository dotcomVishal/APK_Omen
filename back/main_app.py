import streamlit as st
import ollama
import pandas as pd
import pydeck as pdk
import time
import requests
import tempfile

from streamlit_lottie import st_lottie
from core.engine import APKForensics

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="APK Omen | Sovereign Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------

defaults = {
    "analysis_complete": False,
    "report": {},
    "threat_score": 0,
    "ai_brief": "",
    "brief_injected": False,
    "messages": [{"role": "assistant", "content": "Neural link established."}]
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# LOTTIE LOADER
# ---------------------------------------------------

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None

lottie_shield = load_lottieurl("https://lottie.host/8e23337e-6136-4148-9366-22485d454df7/5u4l3y2X5U.json")
lottie_ai     = load_lottieurl("https://lottie.host/5d568c04-727e-400d-953e-5c4d00132a67/M5l4W63y8e.json")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("APK OMEN")

page = st.sidebar.radio("NAVIGATION", [
    "🔍 Forensic Scanner",
    "🧠 Intelligence Node",
    "🌍 Global Threat Globe",
    "🔐 Admin Console"
])

with st.sidebar:
    if lottie_shield:
        st_lottie(lottie_shield, height=110)
    st.caption("Defense Matrix Active")

# ---------------------------------------------------
# 🔍 SCANNER
# ---------------------------------------------------

def render_scanner():

    st.title("APK Scanner")

    uploaded_file = st.file_uploader("Upload APK", type=['apk'])

    if uploaded_file and st.button("🚀 Launch Deep Analysis"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        with st.status("Running Forensics...", expanded=True):

            engine = APKForensics(tmp_path)
            report = engine.generate_report()

            st.session_state.analysis_complete = True
            st.session_state.report = report
            st.session_state.brief_injected = False

            ghost = report.get("ghost_permissions", [])
            secrets = report.get("secrets", [])
            weak_crypto = report.get("weak_crypto", [])

            score = 100
            score -= len(ghost) * 10
            score -= len(secrets) * 15
            score -= len(weak_crypto) * 5

            st.session_state.threat_score = max(0, score)

            st.session_state.ai_brief = f"""
            APK Analysis Summary:

            Package: {report.get('package')}
            Ghost Permissions: {ghost}
            Secrets Found: {secrets}
            Weak Crypto: {weak_crypto}
            OWASP Risks: {report.get('owasp_risks')}
            """

    if st.session_state.analysis_complete:

        report = st.session_state.report

        st.metric("Threat Score", st.session_state.threat_score)

        st.write("OWASP Classification:")
        for risk in report.get("owasp_risks", []):
            st.error(risk)

# ---------------------------------------------------
# 🧠 AI NODE
# ---------------------------------------------------

def render_ai():

    st.title("Neural Intelligence")

    if lottie_ai:
        st_lottie(lottie_ai, height=180)

    # ✅ AUTO INJECT BRIEF (Premium Behaviour)
    if st.session_state.ai_brief and not st.session_state.brief_injected:

        st.session_state.messages.append({
            "role": "user",
            "content": st.session_state.ai_brief
        })

        st.session_state.brief_injected = True

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Query model..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):

            placeholder = st.empty()
            full_resp = ""

            stream = ollama.chat(
                model="deepseek-coder:6.7b",
                messages=st.session_state.messages,
                stream=True
            )

            for chunk in stream:
                content = chunk.get("message", {}).get("content", "")
                full_resp += content
                placeholder.markdown(full_resp + "▌")

            placeholder.markdown(full_resp)

        st.session_state.messages.append({"role": "assistant", "content": full_resp})

# ---------------------------------------------------
# 🌍 GLOBE
# ---------------------------------------------------

def render_globe():

    st.title("Global Threat Monitor")

    data = pd.DataFrame({
        "lat": [37.77, 51.50],
        "lon": [-122.41, -0.12],
        "size": [80000, 60000]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["lon", "lat"],
        get_radius="size",
        get_fill_color=[0, 255, 65, 120],
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=0.8),
        views=[pdk.View(type="GlobeView")]
    )

    st.pydeck_chart(deck)

# ---------------------------------------------------
# 🔐 ADMIN
# ---------------------------------------------------

def render_admin():

    st.title("Admin Console")

    c1, c2, c3 = st.columns(3)
    c1.metric("Users", "1,240")
    c2.metric("Threats", "8,943")
    c3.metric("Load", "14%")

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

if page == "🔍 Forensic Scanner":
    render_scanner()

elif page == "🧠 Intelligence Node":
    render_ai()

elif page == "🌍 Global Threat Globe":
    render_globe()

elif page == "🔐 Admin Console":
    render_admin()
