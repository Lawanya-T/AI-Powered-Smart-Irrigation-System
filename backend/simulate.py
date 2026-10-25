"""
Sensor Data Simulator — Week 1, Task 5
Posts each row of sensor_reading_table_format.csv to your LIVE backend
(http://127.0.0.1:8000/sensor-reading), so your actual database gets
populated the way a real sensor feed would. Run this AFTER:
  1. uvicorn main:app --reload is running
  2. You've registered at least one farmer -> crop -> field via Swagger
     (field_id 1 must exist, or change FIELD_ID_OVERRIDE below)
"""
import pandas as pd
import requests
import time
from pathlib import Path

API_URL = "http://127.0.0.1:8000/sensor-reading"
CSV_PATH = Path(r"C:\Users\lawanya\smart-irrigation-system\data\sensor_reading_table_format.csv")
FIELD_ID_OVERRIDE = None   # set to an int (e.g. 1) to force every row to use that field_id,
                            # matching whatever field you actually created in your DB
DELAY_SECONDS = 0.3        # small delay so it feels like a live stream, not a burst

df = pd.read_csv(CSV_PATH)
success, failed = 0, 0

for _, row in df.iterrows():
    field_id = FIELD_ID_OVERRIDE if FIELD_ID_OVERRIDE is not None else int(row["field_id"])
    payload = {
        "sensor_id": row["sensor_id"],
        "field_id": field_id,
        "moisture_value": float(row["moisture_value"]),
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            success += 1
        else:
            failed += 1
            print(f"Failed ({resp.status_code}): {payload} -> {resp.text}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend. Is uvicorn running on port 8000?")
        break
    time.sleep(DELAY_SECONDS)

print(f"\nDone. {success} readings inserted successfully, {failed} failed.")