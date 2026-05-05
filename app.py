import streamlit as st

from facts import Facts
from rules import load_rules
from engine import forward_chain
from explain import format_explanations
from logger import log_event, get_logs, clear_logs

# -----------------------------
# INIT SYSTEM
# -----------------------------
st.set_page_config(page_title="Smart Home AI", layout="wide")

facts = Facts()
rules = load_rules()

st.title("🏠 Smart Home Rule-Based AI System")

# -----------------------------
# SIDEBAR (USER CONTROL)
# -----------------------------
st.sidebar.header("User Controls")

override = st.sidebar.toggle("Override System")
sleep_time = st.sidebar.slider("Sleep Time", 0, 23, 22)

# -----------------------------
# SENSOR INPUTS
# -----------------------------
st.header("Sensor Inputs")

motion = st.checkbox("Motion detected in kitchen")
time = st.slider("Current Hour", 0, 23, 21)
temperature = st.slider("Temperature", 60, 90, 72)

# -----------------------------
# UPDATE FACTS
# -----------------------------
facts.update("motion_kitchen", motion)
facts.update("time", time)
facts.update("temperature", temperature)
facts.update("override", override)

# log sensor input
log_event("sensor_update", facts.get())

# -----------------------------
# INFERENCE ENGINE
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

# log decisions
log_event("inference_result", {
    "actions": actions,
    "explanations": explanations
})

# -----------------------------
# OUTPUT SECTION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 Actions Taken")

    if actions:
        for a in actions:
            st.write("•", a)
    else:
        st.write("No actions triggered")

with col2:
    st.subheader("🔍 Explainability")

    formatted = format_explanations(explanations)
    for f in formatted:
        st.text(f)

# -----------------------------
# LIVE FACTS VIEW
# -----------------------------
st.subheader("📡 Live System State")
st.json(facts.get())

# -----------------------------
# LOGS SECTION (PERSISTENT)
# -----------------------------
st.subheader("📊 System Logs")

logs = get_logs()

if logs:
    for entry in reversed(logs[-10:]):
        st.write(f"**{entry['timestamp']}**")
        st.write(entry["event_type"])
        st.json(entry["data"])
        st.write("---")
else:
    st.write("No logs yet.")

# -----------------------------
# CLEAR LOGS
# -----------------------------
if st.button("Clear Logs"):
    clear_logs()
    st.rerun()
