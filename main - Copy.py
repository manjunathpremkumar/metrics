import pandas as pd
import numpy as np
import datetime as dt

# --- CONFIG ---
start_date = dt.datetime(2024, 1, 1)
end_date = dt.datetime(2024, 12, 31, 23)  # Hourly data for 1 year
timestamps = pd.date_range(start=start_date, end=end_date, freq='H')


# --- Seasonal multipliers for airline industry (booking peaks etc.) ---
def seasonal_factor(date):
    # Peak booking months: Nov–Jan (holiday), May–July (summer)
    if date.month in [11, 12, 1]:
        return 1.4
    elif date.month in [5, 6, 7]:
        return 1.3
    else:
        return 1.0


# --- Daily load pattern ---
def daily_load(hour):
    if 7 <= hour < 11:
        return 1.0  # average load
    elif 11 <= hour < 13:
        return 1.6  # peak load
    else:
        return 0.7  # non-peak load


# --- Generate random performance metrics ---
data = []
np.random.seed(42)

for ts in timestamps:
    base_tps = 150  # base TPS for login API
    season = seasonal_factor(ts)
    daily = daily_load(ts.hour)

    # TPS with random noise and seasonal/daily variation
    tps = base_tps * season * daily * np.random.uniform(0.85, 1.15)

    # Response time (ms): inversely correlated with TPS, but adds variability
    response_time = np.random.normal(loc=400 - (tps / 3), scale=30)
    response_time = max(80, response_time)

    # CPU (%) roughly correlated with TPS
    cpu = np.clip(np.random.normal(loc=tps / 5, scale=5), 5, 95)

    # Memory (%) – grows slower but steady with small random fluctuations
    memory = np.clip(np.random.normal(loc=60 + (tps / 50), scale=3), 30, 90)

    # JVM heap usage (%) – depends on memory and CPU
    jvm_heap = np.clip(np.random.normal(loc=(memory * 0.8 + cpu * 0.2), scale=5), 20, 95)

    data.append([ts, round(tps, 2), round(response_time, 2), round(cpu, 2),
                 round(memory, 2), round(jvm_heap, 2)])

# --- Create DataFrame ---
df = pd.DataFrame(data, columns=["Timestamp", "TPS", "ResponseTime_ms", "CPU_%", "Memory_%", "JVM_Heap_%"])

# --- Save to CSV ---
df.to_csv("login_service_metrics_2024.csv", index=False)

print("✅ Synthetic data generated: login_service_metrics_2024.csv")
print(df.head(10))
