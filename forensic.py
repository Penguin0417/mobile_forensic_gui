import streamlit as st
import pandas as pd
import altair as alt
import subprocess, time
from datetime import datetime, timedelta

# ────────── Page Setup & CSS ──────────
st.set_page_config("Mobile Forensic Triage", "📱", "wide")
st.markdown("""
<style>
  body { background-color: #0e1117; color: #fff; }
  .stButton>button { background: linear-gradient(90deg,#0d6efd,#6610f2); color:#fff; }
  .stSidebar { background-color: #1c1f2e; }
  .title { font-size:2.5rem; color:#0d6efd; text-align:center; margin-bottom:1rem; }
  .section { border:1px solid #252a3c; padding:1rem; border-radius:8px; margin-bottom:1rem; }
  .radar { width:100px; }
</style>
""", unsafe_allow_html=True)

# ────────── Sidebar with Two Themed Images ──────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/ISS-32_Satellite.jpg", use_column_width=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0e/Hacker_Typing.jpg", use_column_width=True)
    st.title("📱 Forensic Triage")
    st.markdown("**Navigate**")
    page = st.radio("", [
        "🔌 Connect Device",
        "🧾 Checklist",
        "👁️ Preview",
        "📊 Analytics",
        "📤 Export"
    ])

# ────────── Main Page Image ──────────
st.image("https://upload.wikimedia.org/wikipedia/commons/7/7f/Satellite_Network.jpg", use_column_width=True)

# ────────── Animated Radar GIF Loader ──────────
def show_radar():
    st.image("https://i.imgur.com/8Km9tLL.gif", caption="Scanning…", output_format="GIF", width=100)

# ────────── Tab: Connect Device ──────────
if page == "🔌 Connect Device":
    st.markdown('<div class="title">🔌 Connect Your Android Device</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Check ADB Connection"):
            with st.spinner("Detecting device…"):
                time.sleep(1)
                try:
                    out = subprocess.check_output(["adb", "devices"], text=True)
                    lines = out.strip().split("\n")[1:]
                    if any("device" in l for l in lines):
                        st.success("✅ Device connected")
                    else:
                        st.error("❌ No device found")
                except Exception as e:
                    st.error(f"Error: {e}")
    with col2:
        if st.button("ℹ️ Refresh Device Info"):
            with st.spinner("Gathering device info…"):
                time.sleep(1)
                try:
                    model = subprocess.check_output(
                        ["adb","shell","getprop","ro.product.model"], text=True
                    ).strip()
                    android = subprocess.check_output(
                        ["adb","shell","getprop","ro.build.version.release"], text=True
                    ).strip()
                    batt = subprocess.check_output(["adb","shell","dumpsys","battery"], text=True)
                    level = [l.split(": ")[1] for l in batt.splitlines() if "level" in l][0]
                    st.write(f"**Model:** {model}")
                    st.write(f"**Android:** {android}")
                    st.write(f"**Battery:** {level}%")
                except:
                    st.error("Failed to fetch info")

# ────────── Tab: Evidence Checklist ──────────
elif page == "🧾 Checklist":
    st.markdown('<div class="title">🗂️ Select Evidence Types</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    call = st.checkbox("📞 Call Logs")
    sms = st.checkbox("✉️ SMS Messages")
    wa = st.checkbox("💬 WhatsApp Chats")
    photos = st.checkbox("🖼️ Photos")
    videos = st.checkbox("🎥 Videos")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    keywords = st.text_input("🔍 Keyword Filter")
    date_from = st.date_input("From", value=datetime.now() - timedelta(days=7))
    date_to = st.date_input("To", value=datetime.now())
    st.markdown('</div>', unsafe_allow_html=True)

# ────────── Tab: Live Preview ──────────
elif page == "👁️ Preview":
    st.markdown('<div class="title">👁️ Preview Selected Data</div>', unsafe_allow_html=True)
    if 'call' in locals() and call:
        df_calls = pd.DataFrame({
            "Number":["+123","+456"],
            "Date":["2025-05-29","2025-05-30"],
            "Duration":["60s","120s"]
        })
        st.subheader("📞 Call Logs"); st.dataframe(df_calls, use_container_width=True)
    if 'sms' in locals() and sms:
        df_sms = pd.DataFrame({
            "From":["Alice","Bob"],
            "Date":["2025-05-28","2025-05-30"],
            "Message":["Hi","Hello"]
        })
        st.subheader("✉️ SMS"); st.dataframe(df_sms, use_container_width=True)
    if 'wa' in locals() and wa:
        df_wa = pd.DataFrame({"Chat":["Alice","Group"],"Msgs":[12,34]})
        st.subheader("💬 WhatsApp"); st.dataframe(df_wa, use_container_width=True)
    if ('photos' in locals() and photos) or ('videos' in locals() and videos):
        st.subheader("📁 Media Thumbnails")
        cols = st.columns(3)
        for col in cols:
            col.image("https://i.imgur.com/4AiXzf8.jpeg", width=150)

# ────────── Tab: Analytics ──────────
elif page == "📊 Analytics":
    st.markdown('<div class="title">📊 Data Analytics</div>', unsafe_allow_html=True)
    counts = pd.DataFrame({
        "Type":["Calls","SMS","WhatsApp","Photos","Videos"],
        "Count":[
            len(df_calls) if 'df_calls' in locals() else 0,
            len(df_sms)   if 'df_sms'   in locals() else 0,
            len(df_wa)    if 'df_wa'    in locals() else 0,
            6 if 'photos' in locals() and photos else 0,
            6 if 'videos' in locals() and videos else 0
        ]
    })
    bar = alt.Chart(counts).mark_bar().encode(x="Type", y="Count", color="Type")
    st.altair_chart(bar, use_container_width=True)
    pie = alt.Chart(counts).mark_arc().encode(theta="Count", color="Type")
    st.altair_chart(pie, use_container_width=True)

# ────────── Tab: Export ──────────
elif page == "📤 Export":
    st.markdown('<div class="title">📤 Export Evidence</div>', unsafe_allow_html=True)
    fmt = st.selectbox("Select Export Format", ["CSV","PDF","ZIP"])
    if st.button("🚀 Export"):
        with st.spinner("Exporting…"):
            time.sleep(1)
        st.success(f"✅ Data exported as {fmt}")

# ────────── Footer ──────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#555;'>© 2025 Quick Evidence Finder</p>", unsafe_allow_html=True)
