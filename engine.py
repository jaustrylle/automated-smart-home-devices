# Forward chaining inference engine

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
