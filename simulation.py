# Dataset and environment simulation

import pandas as pd

def load_energy_data(path):

    df = pd.read_csv(path)

    df["Energy Consumption (kWh)"] *= 100

    return df


def simulate_time_series(df):

    # Convert dataset into pseudo-events
    events = []

    for _, row in df.head(50).iterrows():

        events.append({
            "time": int(row["Unix Timestamp"] % 24),
            "motion": row["Appliance Usage"] == 1,
            "temperature": row["Voltage"]
        })

    return events
