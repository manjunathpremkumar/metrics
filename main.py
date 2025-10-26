import pandas as pd
import numpy as np
import datetime as dt
import json
import os

# --- CONFIG ---
start_date = dt.datetime(2024, 1, 1)
end_date = dt.datetime(2024, 12, 31, 23)
timestamps = pd.date_range(start=start_date, end=end_date, freq='H')

output_folder = "appd_metrics_json"
os.makedirs(output_folder, exist_ok=True)


# --- Seasonal and daily variations ---
def seasonal_factor(date):
    if date.month in [11, 12, 1]:
        return 1.4
    elif date.month in [5, 6, 7]:
        return 1.3
    else:
        return 1.0


def daily_load(hour):
    if 7 <= hour < 11:
        return 1.0
    elif 11 <= hour < 13:
        return 1.6
    else:
        return 0.7


np.random.seed(42)

# --- Initialize metric containers ---
metrics_data = {
    "TPS": [],
    "ResponseTime_ms": [],
    "CPU_%": [],
    "Memory_%": [],
    "JVM_Heap_%": []
}

# --- Generate data ---
for ts in timestamps:
    season = seasonal_factor(ts)
    daily = daily_load(ts.hour)

    # TPS
    tps = round(150 * season * daily * np.random.uniform(0.85, 1.15), 2)
    metrics_data["TPS"].append({"timestamp": ts.isoformat(), "value": tps})

    # Response Time (ms) - inversely correlated with TPS
    response_time = round(max(80, np.random.normal(loc=400 - (tps / 3), scale=30)), 2)
    metrics_data["ResponseTime_ms"].append({"timestamp": ts.isoformat(), "value": response_time})

    # CPU (%)
    cpu = round(np.clip(np.random.normal(loc=tps / 5, scale=5), 5, 95), 2)
    metrics_data["CPU_%"].append({"timestamp": ts.isoformat(), "value": cpu})

    # Memory (%)
    memory = round(np.clip(np.random.normal(loc=60 + (tps / 50), scale=3), 30, 90), 2)
    metrics_data["Memory_%"].append({"timestamp": ts.isoformat(), "value": memory})

    # JVM Heap (%)
    jvm_heap = round(np.clip(np.random.normal(loc=(memory * 0.8 + cpu * 0.2), scale=5), 20, 95), 2)
    metrics_data["JVM_Heap_%"].append({"timestamp": ts.isoformat(), "value": jvm_heap})

# --- Save each metric as separate JSON file ---
for metric, data_list in metrics_data.items():
    filename = os.path.join(output_folder, f"{metric}_2024.json")
    with open(filename, "w") as f:
        json.dump({"metricName": metric, "dataPoints": data_list}, f, indent=2)

print(f"✅ 5 JSON files generated in folder: {output_folder}")
