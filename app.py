import streamlit as st
from datetime import datetime

from facts import Facts
from rules import load_rules
from engine import forward_chain
from logger import log_event, get_logs, clear_logs
from explain import format_explanations
from learning import run_learning

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Smart Home AI",
    layout="wide",
    page_icon="🏠"
)

# -----------------------------
# INIT SYSTEM
# -----------------------------
facts = Facts()
rules = load_rules()

st.title("🏠 Smart Home AI System")
st.caption("Rule-based forward chaining AI with appliance-aware reasoning")

# -----------------------------
# SIDEBAR (CONTROL PANEL)
# -----------------------------
st.sidebar.header("⚙️ Control Panel")

override = st.sidebar.toggle("🚫 Override System")
sleep_time = st.sidebar.slider("🌙 Sleep Time", 0, 23, 22)

st.sidebar.divider()

st.sidebar.subheader("📡 Sensor Controls")
motion = st.sidebar.checkbox("Motion detected (kitchen)")
time = st.sidebar.slider("Current Hour", 0, 23, 21)
temperature = st.sidebar.slider("Temperature (°F)", 60, 90, 72)

# -----------------------------
# UPDATE FACTS
# -----------------------------
facts.update("motion_kitchen", motion)
facts.update("time", time)
facts.update("temperature", temperature)
facts.update("override", override)

log_event("sensor_update", facts.get())

# -----------------------------
# RUN INFERENCE
# -----------------------------
if not override:
    actions, explanations = forward_chain(facts.get(), rules)
else:
    actions = ["SYSTEM PAUSED"]
    explanations = [{
        "action": "none",
        "rule": "override",
        "why": "User disabled automation"
    }]

log_event("inference_result", {
    "actions": actions,
    "explanations": explanations
})

# -----------------------------
# MAIN DASHBOARD LAYOUT
# -----------------------------
col1, col2, col3 = st.columns(3)

# ---- COLUMN 1: ACTIONS ----
with col1:
    st.subheader("⚡ Actions")

    if actions:
        for a in actions:
            st.success(a)
    else:
        st.info("No actions triggered")

# ---- COLUMN 2: EXPLANATIONS ----
with col2:
    st.subheader("🧠 Reasoning")

    formatted = format_explanations(explanations)

    for f in formatted:
        st.code(f)

# ---- COLUMN 3: SYSTEM STATE ----
with col3:
    st.subheader("📊 Live State")
    st.json(facts.get())

# -----------------------------
# LEARNING SECTION
# -----------------------------
st.divider()

st.subheader("🧠 Learning Engine (Behavior Discovery)")

if st.button("Run Learning Analysis"):

    logs = get_logs()
    suggestions = run_learning(logs)

    if suggestions:

        for s in suggestions:
            st.markdown(f"### 🔹 {s['rule']}")
            st.write("**Logic:**", s["logic"])
            st.write("**Confidence:**", s["confidence"])
            st.divider()

    else:
        st.warning("No patterns found yet")

# -----------------------------
# LOG VIEWER (DEBUG PANEL)
# -----------------------------
with st.expander("📜 System Logs (Debug View)"):

    logs = get_logs()

    if logs:
        for entry in reversed(logs[-15:]):
            st.write(f"**{entry['timestamp']}** — {entry['event_type']}")
            st.json(entry["data"])
            st.divider()
    else:
        st.info("No logs available")

# -----------------------------
# SYSTEM ACTION BAR
# -----------------------------
st.divider()

colA, colB = st.columns(2)

with colA:
    if st.button("🧹 Clear Logs"):
        clear_logs()
        st.success("Logs cleared")

with colB:
    st.button("🔄 Refresh State")
