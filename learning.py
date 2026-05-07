# Simple behavior learning
# Learns patterns from user/system logs to suggest or generate rules.

from collections import Counter


def extract_action_patterns(logs):
    actions = []

    for entry in logs:
        if entry["event_type"] == "inference_result":
            data = entry.get("data", {})
            actions.extend(data.get("actions", []))

    return Counter(actions)


def extract_rule_patterns(logs):
    rules = []

    for entry in logs:
        if entry["event_type"] == "inference_result":
            data = entry.get("data", {})
            explanations = data.get("explanations", [])

            for explanation in explanations:
                rules.append(explanation.get("rule"))

    return Counter(rules)


def extract_time_patterns(logs):
    time_map = {}

    for entry in logs:
        if entry["event_type"] == "sensor_update":
            hour = entry["data"].get("time")

            if hour is not None:
                time_map[hour] = time_map.get(hour, 0) + 1

    return time_map


def suggest_rules(action_counts, rule_counts, time_patterns):
    suggestions = []

    for action, count in action_counts.items():
        if count >= 2 and action == "turn_off_lights":
            suggestions.append({
                "rule": "energy_saving_lights",
                "logic": "if no motion, then turn_off_lights",
                "confidence": count
            })

    for rule, count in rule_counts.items():
        if count >= 3:
            suggestions.append({
                "rule": f"reinforced_{rule}",
                "logic": f"strengthen existing rule: {rule}",
                "confidence": count
            })

    for hour, frequency in time_patterns.items():
        if frequency >= 2 and hour >= 22:
            suggestions.append({
                "rule": "night_mode_auto_detected",
                "logic": f"if time >= {hour}, then activate night behavior",
                "confidence": frequency
            })

    return suggestions


def run_learning(logs):
    action_counts = extract_action_patterns(logs)
    rule_counts = extract_rule_patterns(logs)
    time_patterns = extract_time_patterns(logs)

    return suggest_rules(action_counts, rule_counts, time_patterns)
