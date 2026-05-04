# Explainability layer

def format_explanations(explanations):

    output = []

    for e in explanations:
        output.append(
            f"Action: {e['action']}\n"
            f"Triggered by rule: {e['rule']}\n"
            f"Reason: {e['why']}\n"
        )

    return output
