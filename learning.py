# Simple behavior learning
# Learns patterns from user/system logs to suggest or generate rules

from collections import Counter
from datetime import datetime


# -----------------------------------
# 1. EXTRACT PATTERNS FROM LOGS
# -----------------------------------
def extract_action_patterns(logs):
    """
    Counts how often each action occurs.
    """
    actions = []

    for entry in logs:
        if entry["event_type"] == "inference_result":
            actions.extend(entry["data"]["actions"])

    return Counter(actions)


# -----------------------------------
# 2. DETECT TIME-BASED PATTERNS
# -----------------------------------
def extract_time_patterns(logs):
    """
    Finds which hours actions happen most frequently.
    """
    time_map = {}

    for entry in logs:
        if entry["event_type"] == "sensor_update":
            hour = entry["data"].get("time", None)

            if hour is not None:
                time_map[hour] = time_map.get(hour, 0) + 1

    return time_map


# -----------------------------------
# 3. SUGGEST NEW RULES
# -----------------------------------
def suggest_rules(action_counts, time_patterns, threshold=3):
    """
    Converts patterns into rule suggestions.
    """

    suggested_rules = []

    # Example: frequent "lock_doors"
    for action, count in action_counts.items():

        if count >= threshold:

            if action == "lock_doors":
                suggested_rules.append(
                    {
                        "rule": "auto_lock_night",
                        "logic": "if time >= 23 → lock_doors",
                        "confidence": count
                    }
                )

            if action == "turn_off_kitchen_light":
                suggested_rules.append(
                    {
                        "rule": "energy_saving_lights",
                        "logic": "if no motion → turn_off_lights",
                        "confidence": count
                    }
                )

    # Time-based inference example
    for hour, freq in time_patterns.items():

        if freq >= threshold and hour >= 22:
            suggested_rules.append(
                {
                    "rule": "night_mode_inference",
                    "logic": f"if time >= {hour} → activate night mode",
                    "confidence": freq
                }
            )

    return suggested_rules


# -----------------------------------
# 4. MAIN LEARNING PIPELINE
# -----------------------------------
def run_learning(logs):
    """
    Full learning pipeline.
    """

    action_counts = extract_action_patterns(logs)
    time_patterns = extract_time_patterns(logs)

    return suggest_rules(action_counts, time_patterns)
