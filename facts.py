# Sensor state (facts)

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
