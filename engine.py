# Inference engine

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


def backward_chain(goal, facts, rules):
    matching_rules = [rule for rule in rules if rule.action == goal]

    if not matching_rules:
        return {
            "goal": goal,
            "proved": False,
            "rule": "none",
            "why": "No rule in the knowledge base concludes this goal"
        }

    for rule in matching_rules:
        if rule.condition(facts):
            return {
                "goal": goal,
                "proved": True,
                "rule": rule.name,
                "why": rule.explanation
            }

    return {
        "goal": goal,
        "proved": False,
        "rule": matching_rules[0].name,
        "why": "A matching rule exists, but its conditions are not true for the current facts"
    }
