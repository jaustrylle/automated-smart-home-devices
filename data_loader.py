# CSV loading and preprocessing

import os
import pandas as pd

# data1 = pd.read_csv("datasets/smart_home_energy.csv")
# data2 = pd.read_csv("datasets/smart_home_dataset.csv")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "datasets")


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)
