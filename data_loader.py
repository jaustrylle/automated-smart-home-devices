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

# Drop useless columns
def clean_columns(df):
    drop_cols = ["Transaction ID", "Bandwidth", "Offloading Decision"]

    for col in drop_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    return df

# Normalize time by converting to int hours
def normalize_time(df):

    if "time" in df.columns:
        return df

    if "Unix Timestamp" in df.columns:
        df["time"] = pd.to_datetime(df["Unix Timestamp"], unit='s').dt.hour

    return df

# Convert features to booleans
def create_boolean_features(df):

    # Motion detection
    if "Appliance Usage" in df.columns:
        df["motion"] = df["Appliance Usage"] == 1

    # Night detection
    df["is_night"] = df["time"] >= 22

    # No motion
    df["no_motion"] = ~df["motion"]

    return df

# Normalize temperature and energy
def normalize_values(df):

    if "Temperature" in df.columns:
        df["Temperature"] = df["Temperature"].clip(0, 120)

    if "Energy Consumption (kWh)" in df.columns:
        df["Energy Consumption (kWh)"] = df["Energy Consumption (kWh)"].fillna(0)

    return df

# Handle missing values
def handle_missing(df):
    return df.fillna(method="ffill")

# Convert rows to facts
def row_to_facts(row):

    return {
        "motion_kitchen": bool(row.get("motion", False)),
        "time": int(row.get("time", 0)),
        "temperature": float(row.get("Temperature", 72)),
        "is_night": bool(row.get("is_night", False))
    }

# PREPROCESS DATA FOR DATAFRAME
def preprocess_data(df):

    df = clean_columns(df)
    df = normalize_time(df)
    df = create_boolean_features(df)
    df = normalize_values(df)
    df = handle_missing(df)

    return df
