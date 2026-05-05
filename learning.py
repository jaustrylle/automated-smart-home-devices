# Simple behavior learning
# Learns patterns from user/system logs to suggest or generate rules

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
