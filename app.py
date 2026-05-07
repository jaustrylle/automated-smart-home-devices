import streamlit as st

from facts import Facts
from rules import load_rules
from engine import forward_chain, backward_chain
from logger import log_event, get_logs, clear_logs
from explain import format_explanations
from learning import run_learning


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Smart Home AI",
    layout="wide"
)


# -----------------------------
# INIT SYSTEM
# -----------------------------
facts = Facts()
rules = load_rules()

st.title("Smart Home Rule-Based AI System")
st.caption(
    "A transparent automation demo that shows each smart-home decision, "
    "the rule that triggered it, and the current system state."
)


# -----------------------------
# SIDEBAR (CONTROL PANEL)
# -----------------------------
st.sidebar.header("Control Panel")

override = st.sidebar.toggle("Override System")

st.sidebar.divider()

st.sidebar.subheader("Sensor Controls")
motion = st.sidebar.checkbox("Motion detected (kitchen)")
time = st.sidebar.slider("Current Hour", 0, 23, 21)
temperature = st.sidebar.slider("Temperature (F)", 60, 90, 72)


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
    status = "Automation Active"
else:
    actions = ["SYSTEM PAUSED"]
    status = "System Paused by User"
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
st.subheader("System Status")
st.info(status)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Actions")

    if actions:
        for action in actions:
            st.success(action)
    else:
        st.info("No actions triggered")

with col2:
    st.subheader("Reasoning")

    formatted = format_explanations(explanations)
    for explanation in formatted:
        st.code(explanation)

with col3:
    st.subheader("Live State")
    st.json(facts.get())


# -----------------------------
# BACKWARD CHAINING SECTION
# -----------------------------
st.divider()
st.subheader("Backward Chaining Goal Check")

goal_options = [rule.action for rule in rules]
goal = st.selectbox("Goal to prove", goal_options)
goal_result = backward_chain(goal, facts.get(), rules)

if goal_result["proved"]:
    st.success(f"Goal proved: {goal_result['goal']}")
else:
    st.warning(f"Goal not proved: {goal_result['goal']}")

st.write(f"Rule checked: {goal_result['rule']}")
st.write(f"Reason: {goal_result['why']}")


# -----------------------------
# LEARNING SECTION
# -----------------------------
st.divider()
st.subheader("Learning Engine")

if st.button("Run Learning Analysis"):
    logs = get_logs()
    suggestions = run_learning(logs)

    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"### {suggestion['rule']}")
            st.write("**Logic:**", suggestion["logic"])
            st.write(f"**Observed:** {suggestion['confidence']} times")
            st.divider()
    else:
        st.warning("No patterns found yet")


# -----------------------------
# LOG VIEWER (DEBUG PANEL)
# -----------------------------
with st.expander("System Logs (Debug View)"):
    logs = get_logs()

    if logs:
        for entry in reversed(logs[-15:]):
            st.write(f"**{entry['timestamp']}** - {entry['event_type']}")
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
    if st.button("Clear Logs"):
        clear_logs()
        st.success("Logs cleared")
        st.rerun()

with colB:
    if st.button("Refresh State"):
        st.rerun()
