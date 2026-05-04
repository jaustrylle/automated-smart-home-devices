# Rule definitions (knowledge base)

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
