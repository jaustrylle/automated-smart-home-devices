# data_loader.py

import os
import pandas as pd

# -----------------------------
# BASE PATH SETUP (portable)
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "datasets")


# -----------------------------
# LOAD SINGLE DATASET
# -----------------------------
def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            f"Expected location: {DATA_DIR}"
        )

    return pd.read_csv(path)


# -----------------------------
# OPTIONAL: LOAD ALL DATASETS
# (useful for initialization)
# -----------------------------
def load_all_datasets():
    datasets = {}

    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Datasets folder missing: {DATA_DIR}")

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            datasets[name] = pd.read_csv(os.path.join(DATA_DIR, file))

    return datasets

# facts.py

class Facts:
    def __init__(self):
        self.data = {
            "motion_kitchen": False,
            "time": 21,
            "temperature": 72,
            "override": False
        }

    def update(self, key, value):
        self.data[key] = value

    def get(self):
        return self.data

# rules.py

class Rule:
    def __init__(self, name, condition, action, priority=1, explanation=""):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.explanation = explanation


def load_rules():

    return [

        Rule(
            name="motion_light",
            condition=lambda f: f["motion_kitchen"] and f["time"] >= 22,
            action="turn_on_kitchen_light",
            priority=2,
            explanation="Motion detected at night"
        ),

        Rule(
            name="lock_doors_night",
            condition=lambda f: f["time"] >= 23,
            action="lock_doors",
            priority=3,
            explanation="Late night security rule"
        ),

        Rule(
            name="energy_saving",
            condition=lambda f: not f["motion_kitchen"],
            action="turn_off_lights",
            priority=1,
            explanation="No motion detected"
        )
    ]

# engine.py

def forward_chain(facts, rules):

    actions = []
    explanations = []

    changed = True

    while changed:
        changed = False

        for rule in rules:

            if rule.condition(facts):

                if rule.action not in actions:
                    actions.append(rule.action)
                    explanations.append({
                        "action": rule.action,
                        "rule": rule.name,
                        "why": rule.explanation
                    })

                    changed = True

    return actions, explanations

# explain.py

def format_explanations(explanations):

    output = []

    for e in explanations:
        output.append(
            f"Action: {e['action']}\n"
            f"Triggered by rule: {e['rule']}\n"
            f"Reason: {e['why']}\n"
        )

    return output

# simulation.py

import pandas as pd

def load_energy_data(path):

    df = pd.read_csv(path)

    df["Energy Consumption (kWh)"] *= 100

    return df


def simulate_time_series(df):

    # Convert dataset into pseudo-events
    events = []

    for _, row in df.head(50).iterrows():

        events.append({
            "time": int(row["Unix Timestamp"] % 24),
            "motion": row["Appliance Usage"] == 1,
            "temperature": row["Voltage"]
        })

    return events

# logger.py

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "logs.json")


def log_event(event_type, data):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": data
    }

    # Load existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


def get_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

# learning.py

from collections import Counter

# -----------------------------------
# 1. EXTRACT ACTIONS (FIXED)
# -----------------------------------
def extract_action_patterns(logs):

    actions = []

    for entry in logs:

        if entry["event_type"] == "inference_result":

            data = entry.get("data", {})
            actions.extend(data.get("actions", []))

    return Counter(actions)


# -----------------------------------
# 2. EXTRACT RULE FREQUENCY (NEW - IMPORTANT)
# -----------------------------------
def extract_rule_patterns(logs):

    rules = []

    for entry in logs:

        if entry["event_type"] == "inference_result":

            data = entry.get("data", {})
            explanations = data.get("explanations", [])

            for e in explanations:
                rules.append(e.get("rule"))

    return Counter(rules)


# -----------------------------------
# 3. TIME PATTERNS (IMPROVED)
# -----------------------------------
def extract_time_patterns(logs):

    time_map = {}

    for entry in logs:

        if entry["event_type"] == "sensor_update":

            hour = entry["data"].get("time")

            if hour is not None:
                time_map[hour] = time_map.get(hour, 0) + 1

    return time_map


# -----------------------------------
# 4. RULE GENERATION (NOW WORKS)
# -----------------------------------
def suggest_rules(action_counts, rule_counts, time_patterns):

    suggestions = []

    # --- ACTION-BASED LEARNING ---
    for action, count in action_counts.items():

        if count >= 2:   # LOWER threshold for your dataset

            if action == "turn_off_lights":
                suggestions.append({
                    "rule": "energy_saving_lights",
                    "logic": "if no motion → turn_off_lights",
                    "confidence": count
                })

    # --- RULE-BASED LEARNING ---
    for rule, count in rule_counts.items():

        if count >= 3:

            suggestions.append({
                "rule": f"reinforced_{rule}",
                "logic": f"strengthen existing rule: {rule}",
                "confidence": count
            })

    # --- TIME-BASED LEARNING ---
    for hour, freq in time_patterns.items():

        if freq >= 2 and hour >= 22:

            suggestions.append({
                "rule": "night_mode_auto_detected",
                "logic": f"if time >= {hour} → activate night behavior",
                "confidence": freq
            })

    return suggestions


# -----------------------------------
# 5. MAIN PIPELINE
# -----------------------------------
def run_learning(logs):

    action_counts = extract_action_patterns(logs)
    rule_counts = extract_rule_patterns(logs)
    time_patterns = extract_time_patterns(logs)

    return suggest_rules(action_counts, rule_counts, time_patterns)

# app.py

import streamlit as st

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

st.subheader("🧠 Learned Behavior (AI Suggestions)")

if st.button("Run Learning Engine"):

    logs = get_logs()
    suggestions = run_learning(logs)

    if suggestions:

        for s in suggestions:
            st.write(f"**Rule:** {s['rule']}")
            st.write(f"Logic: {s['logic']}")
            st.write(f"Confidence: {s['confidence']}")
            st.write("---")

    else:
        st.write("No patterns found yet.")

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
