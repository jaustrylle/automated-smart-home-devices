# Streamlit UI (entry point)

import streamlit as st
from facts import Facts
from rules import load_rules
from engine import forward_chain
from explain import format_explanations
from logger import log_event, get_logs, clear_logs

# ----------------------
# INIT SYSTEM
# ----------------------
facts = Facts()
rules = load_rules()

st.title("🏠 Smart Home Rule-Based AI System")

# ----------------------
# SIDEBAR CONTROLS
# ----------------------
st.sidebar.header("User Controls")

facts.update("override", st.sidebar.toggle("Override System"))

sleep_time = st.sidebar.slider("Sleep Time", 0, 23, 22)

# ----------------------
# SENSOR INPUTS
# ----------------------
st.header("Sensor Simulation")

motion = st.checkbox("Motion in Kitchen")
time = st.slider("Current Hour", 0, 23, 21)
temperature = st.slider("Temperature", 60, 90, 72)

facts.update("motion_kitchen", motion)
facts.update("time", time)
facts.update("temperature", temperature)

# ----------------------
# INFERENCE ENGINE
# ----------------------
if not facts.get()["override"]:

    actions, explanations = forward_chain(facts.get(), rules)

else:
    actions = ["SYSTEM PAUSED"]
    explanations = [{
        "action": "none",
        "rule": "override",
        "why": "User disabled automation"
    }]

# ----------------------
# OUTPUT
# ----------------------
st.subheader("🧠 Actions")

for a in actions:
    st.write("•", a)

st.subheader("🔍 Explainability")

for e in format_explanations(explanations):
    st.text(e)

# ----------------------
# SIMPLE LOGIC VIEW
# ----------------------
st.subheader("📡 Live Facts")

st.json(facts.get())
